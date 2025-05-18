from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, name, email, password_hash, role, profile_image_url=None):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.profile_image_url = profile_image_url  # NEW

    # Getters
    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_password_hash(self):
        return self.password_hash

    def get_role(self):
        return self.role

    def get_profile_image_url(self):
        return self.profile_image_url

    # Setters
    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email

    def set_password_hash(self, password_hash):
        self.password_hash = password_hash

    def set_profile_image_url(self, url):
        self.profile_image_url = url

    def check_password(self, password_hash):
        return self.password_hash == password_hash  # Still placeholder

    def to_dict(self):
        return {
            "name": self.get_name(),
            "email": self.get_email(),
            "password_hash": self.get_password_hash(),
            "role": self.get_role(),
            "profile_image_url": self.get_profile_image_url(),
        }


class User(Person):
    def __init__(
        self,
        name,
        email,
        password_hash,
        balance,
        license_number,
        license_expiry,
        profile_image_url=None,
        role="user",
        rental_history={"active": None, "inactive": []},
    ):
        super().__init__(name, email, password_hash, role, profile_image_url)
        self.balance = float(balance)
        self.license_number = license_number  # NEW
        self.license_expiry = license_expiry  # NEW
        self.rental_history = rental_history

    # Getters
    def get_balance(self):
        return self.balance

    def get_license_number(self):
        return self.license_number

    def get_license_expiry(self):
        return self.license_expiry

    def get_rental_history(self):
        return self.rental_history

    def get_active_reservation(self):
        return self.rental_history["active"]

    def get_inactive_reservations(self):
        return self.rental_history["inactive"]

    def get_all_reservations(self):
        reservations = []
        active = self.get_active_reservation()
        if active:
            reservations.append(active)
        inactive = self.get_inactive_reservations()
        if inactive:
            reservations.extend(inactive)
        return reservations

    # Setters
    def set_balance(self, balance):
        self.balance = balance

    def set_license_number(self, license_number):
        self.license_number = license_number

    def set_license_expiry(self, license_expiry):
        self.license_expiry = license_expiry

    def set_rental_history(self, status, reservation_id):
        if status == "active":
            self.rental_history["active"] = reservation_id
        elif status == "inactive":
            self.rental_history["inactive"].append(reservation_id)

    def to_dict(self):
        return super().to_dict() | {
            "balance": float(self.get_balance()),
            "license_number": self.get_license_number(),
            "license_expiry": self.get_license_expiry(),
            "rental_history": self.get_rental_history(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data["email"],
            password_hash=data["password_hash"],
            balance=data["balance"],
            license_number=data["license_number"],
            license_expiry=data["license_expiry"],
            profile_image_url=data.get("profile_image_url"),
            role=data["role"],
            rental_history=data["rental_history"],
        )


class Admin(Person):
    def __init__(
        self, name, email, password_hash, profile_image_url=None, role="admin"
    ):
        super().__init__(name, email, password_hash, role, profile_image_url)

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data["email"],
            password_hash=data["password_hash"],
            profile_image_url=data.get("profile_image_url"),
            role=data["role"],
        )


# Mapping of roles to classes
USER_CLASS_MAP = {"user": User, "admin": Admin}
