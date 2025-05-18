from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from functools import wraps
from io import BytesIO
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    send_file,
    flash,
    make_response,
)
from classes.rentalSystem import RentalSystem
from classes.car import CAR_CLASS_MAP
import uuid
import pdfkit
import csv
import io

app = Flask(__name__)
rentalSystem = RentalSystem()
app.secret_key = "auto-hire-rentals"


# Custom Routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Don't block access to login or register
        if request.endpoint in ["login", "register"]:
            return f(*args, **kwargs)

        if rentalSystem.get_user() is None:
            session.clear()
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}


def generate_csv_response(data, headers, filename):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(data)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-type"] = "text/csv"
    return response


# Page Routes
@app.route("/")
@login_required
def main():
    user = rentalSystem.get_user()
    return render_template("index.html", user=user, role=user.get_role())


@app.route("/login", methods=["GET", "POST"])
def login():
    if rentalSystem.get_user() is not None:
        return redirect(url_for("main"))  # or appropriate route

    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = rentalSystem.load_user_by_email(email)
        if user:
            if check_password_hash(user.get_password_hash(), password):
                rentalSystem.login_user(user)  # Optional: you can also just store user
                session["user_email"] = email
                print("User logged in:", email)
                return jsonify({"success": True, "isAdmin": user.get_role()})
            else:
                return jsonify({"success": False, "error": "password", "message": "Invalid password!"})

        else:
            return jsonify(
                {"success": False, "error": "email", "message": "Email not found!"}
            )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    rentalSystem.logout_user()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    flash("Please register to use the system.", "info")
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        raw_password = data.get("password")
        password_hash = generate_password_hash(raw_password)
        role = data.get("role")
        profile_image_url = data.get("profile_image_url", None)

        user_data = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "role": role,
            "profile_image_url": profile_image_url,
        }

        if role == "user":
            user_data |= {
                "balance": data.get("balance"),
                "license_number": data.get("license_number"),
                "license_expiry": data.get("license_expiry"),
                "rental_history": {"active": None, "inactive": []},
            }

        if rentalSystem.load_user_by_email(email) is None:
            rentalSystem.register_user(user_data)
            return jsonify({"success": True})
        else:
            return jsonify(
                {"success": False, "error": "email", "message": "Email already exists!"}
            )

    return render_template("register.html")


@app.route("/profile")
@login_required
def profile():
    user = rentalSystem.get_user()
    if not user:
        flash("Please log in to access your profile.", "danger")
        return redirect("/login")

    active_res = None
    inactive_res_list = []

    # Only normal users have reservation history
    if user.get_role() == "user":
        active_id = user.get_active_reservation()
        inactive_ids = user.get_inactive_reservations()

        active_res = (
            rentalSystem.get_reservation_by_id(active_id) if active_id else None
        )
        inactive_res_list = [
            rentalSystem.get_reservation_by_id(rid) for rid in inactive_ids
        ]

    return render_template(
        "profile.html",
        user=user,
        active_res=active_res,
        inactive_reservations=inactive_res_list,
    )


@app.route("/edit-profile", methods=["POST"])
def edit_profile():
    user = rentalSystem.get_user()
    if not user:
        flash("You must be logged in to update your profile.", "danger")
        return redirect("/login")

    # Basic fields (both user and admin)
    name = request.form.get("name").strip()
    profile_image = request.form.get("profile_image").strip()

    user.set_name(name)
    user.set_profile_image_url(
        profile_image
    )  # Assuming attribute is public or has a setter

    # Extra fields for user role
    if user.get_role() == "user":
        balance = request.form.get("balance").strip()
        license_number = request.form.get("license_number").strip()
        license_expiry = request.form.get("license_expiry").strip()

        user.set_balance(float(balance))
        user.set_license_number(license_number)
        user.set_license_expiry(license_expiry)

    # Save the changes
    rentalSystem.update_user(user)

    flash("Profile updated successfully.", "success")
    return redirect("/profile")


@app.route("/delete-account", methods=["POST"])
def delete_account():
    user = rentalSystem.get_user()
    if not user:
        flash("You must be logged in to delete your account.", "danger")
        return redirect("/login")

    # Delete from file (users.json)
    rentalSystem.delete_user(user.get_email())

    # Clear session
    session.clear()

    return redirect("/logout")


@app.route("/return-car", methods=["POST"])
def return_car():
    user = rentalSystem.get_user()
    if not user:
        flash("Please log in.", "danger")
        return redirect("/login")

    reservation = rentalSystem.get_reservation_by_id(user.get_active_reservation())
    if not reservation:
        flash("No active reservation found.", "warning")
        return redirect("/profile")

    car = rentalSystem.fleet.get_car_by_vin(reservation.get_car_vin())
    today = date.today()
    scheduled_end = reservation.get_end_date()

    # Late or early return logic
    message = ""
    if today > scheduled_end:
        late_days = (today - scheduled_end).days
        fee = late_days * 1000
        user.set_balance(user.get_balance() - fee)
        message = (
            f"Returned late by {late_days} day(s). PKR {fee} deducted as late fee."
        )
    elif today < scheduled_end:
        early_days = (scheduled_end - today).days
        refund = early_days * 500
        user.set_balance(user.get_balance() + refund)
        message = f"Returned early. PKR {refund} refunded to your balance."

    # Update reservation and car
    reservation.set_return_date(date.today())
    reservation.set_status("inactive")
    user.set_rental_history("inactive", reservation.get_id())
    user.set_rental_history("active", None)
    car.set_rental_history("inactive", reservation.get_id())
    car.set_rental_history("delete", reservation.get_id())

    rentalSystem.save_all(user)

    flash("Car returned successfully. " + message, "success")
    return redirect("/profile")


@app.route("/admin-fleet")
@login_required
def manage_fleet():
    if "user_email" in session:
        user = rentalSystem.get_user()
        if user and user.get_role() == "admin":
            cars = rentalSystem.get_cars()
            if not cars:
                cars = []
            return render_template(
                "admin-fleet.html", user=user, role=user.get_role(), cars=cars
            )
        else:
            return "Access Denied", 403
    return "Access Denied", 403


@app.route("/admin/add_car", methods=["POST"])
@login_required
def add_car():
    if not rentalSystem.get_isAdmin():
        return redirect(url_for("login"))

    form = request.form
    category = form.get("car_type")  # "EconomyCar", "LuxuryCar", etc.

    CarClass = CAR_CLASS_MAP.get(category)
    if not CarClass:
        return "Invalid car type", 400

    # Gather shared fields
    vin = form.get("vin")
    model = form.get("model")
    base_rate = float(form.get("base_rate"))
    img_url = form.get("img_url")
    seating_capacity = int(form.get("seating_capacity"))
    colour = form.get("colour")
    car_type = form.get("car_type")  # optional duplication
    rental_history = {"active": [], "inactive": []}

    # Parse features as dict
    features = {
        "air_conditioning": "features[air_conditioning]" in form,
        "bluetooth": "features[bluetooth]" in form,
        "gps": "features[gps]" in form,
        "usb_ports": "features[usb_ports]" in form,
        "sunroof": "features[sunroof]" in form,
        "rear_camera": "features[rear_camera]" in form,
    }

    # Category-specific attributes
    extra_attr = {}
    if category == "EconomyCar":
        extra_attr["fuel_efficiency"] = float(form.get("fuel_efficiency", 0))
    elif category == "LuxuryCar":
        extra_attr["chauffeur_available"] = form.get("chauffeur_available") == "1"
    elif category == "CommercialCar":
        extra_attr["cargo_capacity"] = float(form.get("cargo_capacity", 0))

    # Create car object dynamically
    car = CarClass(
        vin=vin,
        model=model,
        base_rate=base_rate,
        img_url=img_url,
        seating_capacity=seating_capacity,
        colour=colour,
        car_type=car_type,
        features=features,
        **extra_attr,
        rental_history=rental_history,
    )

    # Add to fleet and save
    rentalSystem.fleet.add_car(car)
    rentalSystem.fleet.save_cars()

    return redirect(url_for("manage_fleet"))


@app.route("/admin/edit_car/<vin>", methods=["POST"])
def edit_car(vin):
    car = rentalSystem.fleet.get_car_by_vin(vin)
    if not car:
        return redirect(url_for("manage_fleet"))

    form = request.form
    car.set_model(form.get("model"))
    car.set_base_rate(float(form.get("base_rate")))
    car.set_img_url(form.get("img_url"))
    car.set_seating_capacity(int(form.get("seating_capacity")))
    car.set_colour(form.get("colour"))
    car.set_car_type(form.get("car_type"))

    car.set_features(
        {
            "air_conditioning": "features[air_conditioning]" in form,
            "bluetooth": "features[bluetooth]" in form,
            "gps": "features[gps]" in form,
            "usb_ports": "features[usb_ports]" in form,
            "sunroof": "features[sunroof]" in form,
            "rear_camera": "features[rear_camera]" in form,
        }
    )

    if car.__class__.__name__ == "EconomyCar":
        car.set_fuel_efficiency(float(form.get("fuel_efficiency", 0)))
    elif car.__class__.__name__ == "LuxuryCar":
        car.set_chauffeur_available(form.get("chauffeur_available") == "1")
    elif car.__class__.__name__ == "CommercialCar":
        car.set_cargo_capacity(float(form.get("cargo_capacity", 0)))

    rentalSystem.fleet.save_cars()
    return redirect(url_for("manage_fleet"))


@app.route("/admin/delete_car/<vin>", methods=["POST"])
def delete_car(vin):
    if not rentalSystem.get_isAdmin:
        return redirect("/login")

    success = rentalSystem.fleet.remove_car(vin)
    if success:
        rentalSystem.fleet.save_cars()
    else:
        pass

    return redirect(url_for("manage_fleet"))


@app.route("/admin-report")
@login_required
def admin_reports():
    user = rentalSystem.get_user()
    if not user or user.get_role() != "admin":
        flash("Access restricted to administrators.", "danger")
        return redirect("/")

    # Gather report data
    users = rentalSystem.get_all_users()
    reservations = rentalSystem.get_all_reservations()
    cars = rentalSystem.fleet.get_cars()

    # Filter reservations and users
    current_rentals = []
    reserved_cars = []

    for u in users:
        if u.get_role() == "user":
            active_res_id = u.get_active_reservation()
            if active_res_id:
                res = rentalSystem.get_reservation_by_id(active_res_id)
                if res:
                    current_rentals.append(
                        {
                            "name": u.get_name(),
                            "email": u.get_email(),
                            "car_vin": res.get_car_vin(),
                            "start_date": res.get_start_date(),
                            "end_date": res.get_end_date(),
                        }
                    )

    for car in cars:
        active = car.get_active_reservation()
        if active:
            for res_id in active:
                res = rentalSystem.get_reservation_by_id(res_id)
                if res:
                    reserved_cars.append(
                        {
                            "vin": car.get_vin(),
                            "model": car.get_model(),
                            "user_email": res.get_user_email(),
                            "start_date": res.get_start_date(),
                            "end_date": res.get_end_date(),
                        }
                    )

    return render_template(
        "admin-reports.html",
        current_rentals=current_rentals,
        reserved_cars=reserved_cars,
        user=user,
        role=user.get_role()
    )


@app.route("/admin/download/customers")
def download_customers_report():
    user = rentalSystem.get_user()
    if not user or user.get_role() != "admin":
        return redirect("/")

    data = []
    all_users = rentalSystem.get_all_users()

    for u in all_users:
        if u.get_role() != "user":  # ✅ Skip admin users
            continue

        res_id = u.get_active_reservation()
        if res_id:
            res = rentalSystem.get_reservation_by_id(res_id)
            if res:
                data.append(
                    [
                        u.get_name(),
                        u.get_email(),
                        res.get_car_vin(),
                        res.get_start_date().strftime("%Y-%m-%d"),
                        res.get_end_date().strftime("%Y-%m-%d"),
                    ]
                )

    return generate_csv_response(
        data,
        ["Name", "Email", "Car VIN", "Start Date", "End Date"],
        "customers_report.csv",
    )


@app.route("/admin/download/reserved-cars")
def download_reserved_cars_report():
    user = rentalSystem.get_user()
    if not user or user.get_role() != "admin":
        return redirect("/")

    data = []
    for car in rentalSystem.fleet.get_cars():
        active = car.get_active_reservation()
        if active:
            for res_id in active:
                res = rentalSystem.get_reservation_by_id(res_id)
                if res:
                    data.append(
                        [
                            car.get_vin(),
                            car.get_model(),
                            res.get_user_email(),
                            res.get_start_date(),
                            res.get_end_date(),
                        ]
                    )

    return generate_csv_response(
        data,
        ["VIN", "Model", "User Email", "Start Date", "End Date"],
        "reserved_cars_report.csv",
    )


@app.route("/cars")
@login_required
def available_cars():
    user = rentalSystem.get_user()

    # ✅ Only check reservation status if user is not an admin
    if user and user.get_role() == "user" and user.get_active_reservation():
        flash("You already have an active reservation. Please return the car to reserve another.", "warning")
        return redirect("/profile")  # or /my-reservation

    # Get dates from query params
    start_str = request.args.get("start")
    end_str = request.args.get("end")
    car_type = request.args.get("type")

    # Validate dates
    if not start_str or not end_str:
        flash("Start and end dates are required.", "danger")
        return redirect("/")

    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
        assert start_date <= end_date
    except:
        flash("Invalid date selection.", "danger")
        return redirect("/")

    # Get all cars from fleet
    filtered_cars = rentalSystem.get_available_cars(start_date, end_date)
    if car_type:
        filtered_cars = [car for car in filtered_cars if car.get_car_type() == car_type]

    return render_template(
        "available-cars.html",
        user=user,
        available_cars=filtered_cars,
        start_date=start_str,
        end_date=end_str,
        selected_type=car_type,
    )


@app.route("/cars/<vin>")
@login_required
def car_details(vin):
    user = rentalSystem.get_user()
    start = request.args.get("start")
    end = request.args.get("end")

    # Find car by VIN
    car = rentalSystem.fleet.get_car_by_vin(vin)
    if not car:
        # flash("Car not found.", "danger")
        return redirect("/cars")

    return render_template("car_details.html", user=user, car=car, start=start, end=end)


@app.route("/reserve/<vin>", methods=["GET", "POST"])
@login_required
def reserve_car(vin):
    car = rentalSystem.fleet.get_car_by_vin(vin)
    if not car:
        flash("Car not found.", "danger")
        return redirect("/cars")

    user = rentalSystem.get_user()
    if not user:
        return redirect("/login")

    # ✅ Check: if admin, deny reservation
    if not user or user.get_role() == "admin":
        flash(
            "Admins cannot make reservations. Please log in as a user to book cars.",
            "danger",
        )
        return redirect("/")

    start_date = request.args.get("start")
    end_date = request.args.get("end")

    # Parse dates
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    days = (end - start).days + 1

    if request.method == "POST":
        # Confirm logic
        if user.get_license_expiry() < date.today().isoformat():
            flash("License is expired. Please update before booking.", "danger")
            return redirect(request.url)

        total_cost = car.calculate_rental_cost(days)
        if float(user.get_balance()) < total_cost:
            flash("Insufficient balance to complete reservation.", "danger")
            return redirect(request.url)

        # Deduct balance, set active reservation

        reservation = {
            "id": str(uuid.uuid4()),
            "user_email": user.get_email(),
            "car_vin": car.get_vin(),
            "start_date": start_date,
            "end_date": end_date,
            "cost": total_cost,
            "status": "active",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        rentalSystem.make_reservation(reservation)

        # Generate PDF from HTML
        html = render_template(
            "receipt.html",
            user=user,
            reservation=rentalSystem.get_reservation_by_id(reservation["id"]),
            car=car,
            time=datetime.now(),
            logo=url_for("static", filename="images/logo.png"),
        )
        pdf = pdfkit.from_string(html, False)  # generate in-memory

        # Store PDF in session or disk temporarily
        pdf_bytes = BytesIO(pdf)
        filename = f"Reservation_{reservation['id']}.pdf"

        # Save to session or return directly
        # Save reservation to file/session first
        session["last_reservation_id"] = reservation["id"]
        return redirect(url_for("reservation_success"))

    total_cost = car.calculate_rental_cost(days)

    return render_template(
        "reserve-car.html",
        car=car,
        user=user,
        start=start_date,
        end=end_date,
        days=days,
        cost=total_cost,
    )


@app.route("/receipt/<reservation_id>")
def download_receipt(reservation_id):
    rentalSystem.load_reservations()
    user = rentalSystem.get_user()
    if not user:
        print("User not logged in.")
        flash("You must be logged in to download your receipt.", "danger")
        return redirect("/login")

    reservation = rentalSystem.get_reservation_by_id(user.get_active_reservation())
    if not reservation:
        print("No active reservation found.")
        flash("No active reservation found.", "danger")
        return redirect("/")

    if reservation.get_id() != reservation_id:
        print(
            f"Reservation ID mismatch: expected {reservation.get_id()} but got {reservation_id}"
        )
        flash("Invalid reservation ID.", "danger")
        return redirect("/")

    car = rentalSystem.fleet.get_car_by_vin(reservation.get_car_vin())
    if not car:
        print("Car not found for reservation.")
        flash("Car not found for this reservation.", "danger")
        return redirect("/")

    try:
        html = render_template(
            "receipt.html",
            user=user,
            reservation=reservation,
            car=car,
            time=datetime.now(),
        )
        pdf = pdfkit.from_string(html, False)

        return send_file(
            BytesIO(pdf),
            as_attachment=True,
            download_name=f"Reservation_{reservation_id}.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        print("PDF generation error:", e)
        flash("Error generating PDF receipt.", "danger")
        return redirect("/")


@app.route("/reservation-success")
def reservation_success():
    user = rentalSystem.get_user()
    reservation = rentalSystem.get_reservation_by_id(user.get_active_reservation())
    return render_template(
        "reservation-success.html", reservation=reservation, user=user
    )


# Main program
if __name__ == "__main__":
    app.run(debug=True)
