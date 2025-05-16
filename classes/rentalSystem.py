from helpers.file_handler import FileHandler
from classes.fleet import Fleet
from classes.user import USER_CLASS_MAP

class RentalSystem:

    fileHandler = FileHandler()

    def __init__(self):
        self.user = None
        self.isAdmin = False
        self.fleet = Fleet()

    # Getters
    def get_user(self):
        return self.user
    def get_isAdmin(self):
        return self.isAdmin

    # Methods
    def login_user(self, user, password):
        if user:
            if not user.check_password(password):
                return False
            self.user = user
            self.isAdmin = user.get_role() == "admin"
            return True
        return False

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

