from helpers.file_handler import FileHandler
from classes.fleet import Fleet
from classes.user import USER_CLASS_MAP
from classes.reservation import Reservation


class RentalSystem:

    fileHandler = FileHandler()

    def __init__(self):
        self.user = None
        self.isAdmin = False
        self.fleet = Fleet()
        self.reservations = []
        self.load_reservations()

    # Getters
    def get_user(self):
        return self.user

    def get_isAdmin(self):
        return self.isAdmin

    def get_cars(self):
        return self.fleet.get_cars()

    def get_car_by_vin(self, vin):
        return self.fleet.get_car_by_vin(vin)

    # Methods
    # Handling User
    def register_user(self, user_data):
        users = RentalSystem.fileHandler.load_data("users")

        # Determine user class from role
        role = user_data.get("role").lower()
        user_class = USER_CLASS_MAP.get(role)

        # Create the object
        user_obj = user_class.from_dict(user_data)

        # Add role to saved data explicitly
        user_dict = user_obj.to_dict()
        user_dict["role"] = role

        users.append(user_dict)
        RentalSystem.fileHandler.save_data("users", users)

        return user_obj

    def login_user(self, user, password):
        if user:
            if not user.check_password(password):
                return False
            self.user = user
            self.isAdmin = user.get_role() == "admin"
            return True
        return False
    
    def get_all_users(self):
        users = RentalSystem.fileHandler.load_data("users")
        user_objects = []
        for user_data in users:
            role = user_data.get("role", "user").lower()
            user_class = USER_CLASS_MAP.get(role)
            user_objects.append(user_class.from_dict(user_data))
        return user_objects

    def logout_user(self):
        self.user = None
        self.isAdmin = False

    def load_user_by_email(self, email):
        users = RentalSystem.fileHandler.load_data("users")
        for user_data in users:
            if user_data["email"] == email:
                role = user_data.get("role", "user").lower()
                user_class = USER_CLASS_MAP.get(role)
                return user_class.from_dict(user_data)
        return None

    def update_user(self, user):
        email = user.get_email()
        users = RentalSystem.fileHandler.load_data("users")
        for i in range(len(users)):
            if users[i]["email"] == email:
                users[i] = user.to_dict()
        RentalSystem.fileHandler.save_data("users", users)

    def delete_user(self, email):
        users = RentalSystem.fileHandler.load_data("users")
        user = self.load_user_by_email(email)

        if not user:
            print(f"No user found with email: {email}")
            return

        # If normal user, clean up their reservations and associated car links
        if user.get_role() == "user":
            reservations = user.get_all_reservations()  # Includes active + inactive

            for reservation in reservations:
                # Remove reservation from the car
                car = self.fleet.get_car_by_vin(reservation.get_car_vin())
                if car:
                    car.delete_reservation(reservation.get_id())

                # Remove reservation from reservation list
                self.delete_reservation(reservation)

        # Remove the user from the list
        users = [u for u in users if u["email"] != email]

        # Save updated users and fleet
        self.fleet.save_cars()
        RentalSystem.fileHandler.save_data("users", users)

        self.logout_user()
        print(f"User '{email}' deleted successfully.")

    # Handling Cars
    def get_available_cars(self, start_date, end_date):
        available_cars = []

        for car in self.fleet.get_cars():
            is_available = True
            active_reservations = car.get_active_reservation()

            if active_reservations:
                for reservation_id in active_reservations:
                    res = self.get_reservation_by_id(reservation_id)
                    if res:
                        # Check for overlap
                        if not (
                            res.get_end_date() < start_date
                            or res.get_start_date() > end_date
                        ):
                            is_available = False
                            break  # No need to check other reservations

            if is_available:
                available_cars.append(car)

        return available_cars

    # Handling Reservations
    def load_reservations(self):
        reservations = RentalSystem.fileHandler.load_data("reservations")
        for reservation in reservations:
            reservation_obj = Reservation.from_dict(reservation)
            self.reservations.append(reservation_obj)
    
    def get_all_reservations(self):
        self.load_reservations()
        return self.reservations

    def get_reservation_by_id(self, reservation_id):
        for reservation in self.reservations:
            if reservation.get_id() == reservation_id:
                return reservation
        return None

    def delete_reservation(self, reservation_id):
        for i in range(len(self.reservations)):
            if self.reservations[i].get_id() == reservation_id:
                del self.reservations[i]
                break
        RentalSystem.fileHandler.save_data(
            "reservations", [res.to_dict() for res in self.reservations]
        )

    def make_reservation(self, reservation):
        reservation = Reservation.from_dict(reservation)
        reservations = RentalSystem.fileHandler.load_data("reservations")
        reservations.append(reservation.to_dict())
        RentalSystem.fileHandler.save_data("reservations", reservations)

        self.user.set_rental_history("active", reservation.get_id())
        self.user.set_balance(self.user.get_balance() - reservation.get_cost())
        self.update_user(self.user)

        self.fleet.get_car_by_vin(reservation.get_car_vin()).set_rental_history(
            "active", reservation.get_id()
        )
        self.fleet.save_cars()

        self.load_reservations()

    # Other
    def save_all(self, user):
        RentalSystem.fileHandler.save_data(
            "reservations", [res.to_dict() for res in self.reservations]
        )
        self.fleet.save_cars()
        self.update_user(user)