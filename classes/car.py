from abc import ABC, abstractmethod

class Car(ABC):
    def __init__(self, vin, model, base_rate, img_url, rental_history={'active': None, 'inactive': []}):
        self.vin = vin
        self.model = model
        self.base_rate = base_rate
        self.img_url = img_url
        self.rental_history = rental_history
    
    # Getters
    def get_vin(self):
        return self.vin
    def get_model(self):
        return self.model
    def get_base_rate(self):
        return self.base_rate
    def get_img_url(self):
        return self.img_url
    def get_active_reservation(self):
        return self.rental_history['active']
    def get_inactive_reservations(self):
        return self.rental_history['inactive']

    # Setters
    def set_vin(self, vin):
        self.vin = vin
    def set_model(self, model):
        self.model = model
    def set_base_rate(self, base_rate):
        self.base_rate = base_rate
    def set_img_url(self, img_url):
        self.img_url = img_url
    def set_rental_history(self, status, reservation):
        if status == 'active':
            self.rental_history['active'] = reservation
        elif status == 'inactive':
            self.rental_history['inactive'].append(reservation)
    
    # Abstract methods
    @abstractmethod
    def calculate_rental_cost(self, days):
        pass
    
    # Methods
    def to_dict(self):
        return {
            'vin': self.get_vin(),
            'model': self.get_model(),
            'base_rate': self.get_base_rate(),
            'img_url': self.get_img_url(),
            'category': self.__class__.__name__,
            'rental_history': self.rental_history
        }

class EconomyCar(Car):
    def __init__(self, vin, model, base_rate, img_url, fuel_efficiency, rental_history={'active': None, 'inactive': []}):
        super().__init__(vin, model, base_rate, img_url, rental_history)
        self.fuel_efficiency = fuel_efficiency  # kilometres per litre

    # Getters
    def get_fuel_efficiency(self):
        return self.fuel_efficiency
    
    # Setters
    def set_fuel_efficiency(self, fuel_efficiency):
        self.fuel_efficiency = fuel_efficiency

    # Methods
    def calculate_rental_cost(self, days):
        return (self.base_rate + (self.fuel_efficiency * 100)) * days
    
    def to_dict(self):
        return super().to_dict() | {'fuel_efficiency': self.get_fuel_efficiency()}
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            vin=data['vin'],
            model=data['model'],
            base_rate=data['base_rate'],
            img_url=data['img_url'],
            fuel_efficiency=data['fuel_efficiency'],
            rental_history=data['rental_history']
        )

class LuxuryCar(Car):
    def __init__(self, vin, model, base_rate, img_url, chauffeur_available, rental_history={'active': None, 'inactive': []}):
        super().__init__(vin, model, base_rate, img_url, rental_history)
        self.chauffeur_available = chauffeur_available
    
    # Getters
    def get_chauffeur_available(self):
        return self.chauffeur_available

    # Setters
    def set_chauffeur_available(self, chauffeur_available):
        self.chauffeur_available = chauffeur_available

    # Methods
    def calculate_rental_cost(self, days):
        return (self.base_rate + (int(self.chauffeur_available) * 3000)) * days
    
    def to_dict(self):
        return super().to_dict() | {'chauffeur_available': self.get_chauffeur_available()}
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            vin=data['vin'],
            model=data['model'],
            base_rate=data['base_rate'],
            img_url=data['img_url'],
            chauffeur_available=data['chauffeur_available'],
            rental_history=data['rental_history']
        )
    
class CommercialCar(Car):
    def __init__(self, vin, model, base_rate, img_url, cargo_capacity, rental_history={'active': None, 'inactive': []}):
        super().__init__(vin, model, base_rate, img_url, rental_history)
        self.cargo_capacity = cargo_capacity  # in kg

    # Getters
    def get_cargo_capacity(self):
        return self.cargo_capacity
    
    # Setters
    def set_cargo_capacity(self, cargo_capacity):
        self.cargo_capacity = cargo_capacity

    # Methods
    def calculate_rental_cost(self, days):
        return (self.base_rate + (self.cargo_capacity * 10)) * days
    
    def to_dict(self):
        return super().to_dict() | {'cargo_capacity': self.get_cargo_capacity()}
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            vin=data['vin'],
            model=data['model'],
            base_rate=data['base_rate'],
            img_url=data['img_url'],
            cargo_capacity=data['cargo_capacity'],
            rental_history=data['rental_history']
        )

# Mapping of car categories to classes    
CAR_CLASS_MAP = {
    "EconomyCar": EconomyCar,
    "LuxuryCar": LuxuryCar,
    "CommercialCar": CommercialCar
}
