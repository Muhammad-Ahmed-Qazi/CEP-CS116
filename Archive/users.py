from abc import ABC, abstractmethod
import bcrypt

class Person(ABC):
    def __init__(self, first_name, last_name, email, password, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = self.hash_password(password)
        self.phone_number = phone_number
        self.role = None
        # self.is_authenticated = False
    
    # Getter methods
    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_email(self):
        return self._email

    def get_password(self):
        return self.password_hash

    def get_phone_number(self):
        return self._phone_number

    # Setter methods
    def set_first_name(self, value):
        self._first_name = value

    def set_last_name(self, value):
        self._last_name = value

    def set_email(self, value):
        self._email = value

    def set_password(self, value):
        self.password_hash = self.hash_password(value)

    def set_phone_number(self, value):
        self._phone_number = value
    
    def hash_password(self, plain_password):
        return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password_hash)

class User(Person):
    def __init__(self, first_name, last_name, email, password, phone_number, license_number, license_expiry, current_reservation, balance):
        super().__init__(first_name, last_name, email, password, phone_number)
        self.role = "user"
        self.license_number = license_number
        self.license_expiry = license_expiry
        self.current_reservation = current_reservation
        self.rental_history = []
        self.balance = balance
    
    # Getter methods
    def get_license_number(self):
        return self.license_number

    def get_license_expiry(self):
        return self.license_expiry

    def get_current_reservation(self):
        return self.current_reservation

    def get_rental_history(self):
        return self.rental_history

    def get_balance(self):
        return self.balance

    # Setter methods
    def set_license_number(self, value):
        self.license_number = value

    def set_license_expiry(self, value):
        self.license_expiry = value

    def set_current_reservation(self, value):
        self.current_reservation = value

    def set_rental_history(self, reservation):
        self.rental_history.append(reservation)

    def set_balance(self, value):
        self.balance = value

class Admin(Person):
    def __init__(self, first_name, last_name, email, password, phone_number):
        super().__init__(first_name, last_name, email, password, phone_number)
        self.role = "admin"