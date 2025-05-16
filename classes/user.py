from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, email, password_hash, role):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
    
    # Getters
    def get_name(self):
        return self.name
    def get_email(self):
        return self.email
    def get_password_hash(self):
        return self.password_hash
    def get_role(self):
        return self.role
    
    # Setters
    def set_name(self, name):
        self.name = name
    def set_email(self, email):
        self.email = email
    def set_password_hash(self, password_hash):
        self.password_hash = password_hash

    # Abstract methods


    # Methods
    def check_password(self, password_hash):
        return self.password_hash == password_hash  # In a real-world scenario, use a secure hash comparison
    
    # Methods
    def to_dict(self):
        return {
            'name': self.get_name(),
            'email': self.get_email(),
            'password_hash': self.get_password_hash(),
            'role': self.get_role()
        }
    

class User(Person):
    def __init__(self, name, email, password_hash, balance, role='user', rental_history={'active': None, 'inactive': []}):
        super().__init__(name, email, password_hash, role)
        self.balance = balance
        self.rental_history = rental_history  # {'active': None, 'inactive': []}
    
    # Getters
    def get_rental_history(self):
        return self.rental_history
    def get_balance(self):
        return self.balance
    def get_active_reservation(self):
        return self.rental_history['active']
    def get_inactive_reservations(self):
        return self.rental_history['inactive']

    # Setters
    def set_balance(self, balance):
        self.balance = balance
    def set_rental_history(self, status, reservation):
        if status == 'active':
            self.rental_history['active'] = reservation
        elif status == 'inactive':
            self.rental_history['inactive'].append(reservation)
    
    # Methods
    def to_dict(self):
        return super().to_dict() | {
            'balance': self.get_balance(),
            'rental_history': self.get_rental_history()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            email=data['email'],
            password_hash=data['password_hash'],
            balance=data['balance'],
            role=data['role'],
            rental_history=data['rental_history']
        )


class Admin(Person):
    def __init__(self, name, email, password_hash, role='admin'):
        super().__init__(name, email, password_hash, role)

    # Methods
    def to_dict(self):
        return super().to_dict()
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            email=data['email'],
            password_hash=data['password_hash'],
            role=data['role']
        )

# Mapping of roles to classes   
USER_CLASS_MAP = {
    "user": User,
    "admin": Admin
}