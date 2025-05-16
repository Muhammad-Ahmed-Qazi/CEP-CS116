from flask import Flask, render_template, request, jsonify, session
from classes.rentalSystem import RentalSystem

app = Flask(__name__)
rentalSystem = RentalSystem()
app.secret_key = "auto-hire-rentals"


# Page Routes
@app.route("/")
def main():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = rentalSystem.load_user_by_email(email)
        if user:
            if rentalSystem.login_user(user, password):
                session['user_email'] = email
                return jsonify({"success": True, "isAdmin": user.get_role()})
            else:
                return jsonify({"success": False, "error": "password", "message": "Invalid password!"})
        else:
            return jsonify({"success": False, "error": "email", "message": "Email not found!"})

    return render_template("login.html")    

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        user_data = {
            "name": name,
            "email": email,
            "password_hash": password,  # In a real app, hash the password
            "role": role
        }

        if role == 'user':
            user_data = user_data | {
                "balance": data.get("balance"),
                "rental_history": {
                    "active": None,
                    "inactive": []
                }
            }

        if rentalSystem.load_user_by_email(email) is None:
            # Register the user
            rentalSystem.register_user(user_data)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "email", "message": "Email already exists!"})
    
    return render_template("register.html")

# Custom Routes
 
    
# Main program
if __name__ == "__main__":
    app.run(debug=True)