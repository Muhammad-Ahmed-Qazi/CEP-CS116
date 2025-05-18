from abc import ABC, abstractmethod

class Car(ABC):
    def __init__(self, vin, model, base_rate, img_url, seating_capacity, colour, car_type, features, rental_history={'active': None, 'inactive': []}):
        self.vin = vin
        self.model = model
        self.base_rate = base_rate
        self.img_url = img_url
        self.seating_capacity = seating_capacity
        self.colour = colour
        self.car_type = car_type
        self.features = features
        self.rental_history = rental_history

    # Getters
    def get_vin(self): return self.vin
    def get_model(self): return self.model
    def get_base_rate(self): return self.base_rate
    def get_img_url(self): return self.img_url
    def get_seating_capacity(self): return self.seating_capacity
    def get_colour(self): return self.colour
    def get_car_type(self): return self.car_type
    def get_features(self): return self.features
    def get_active_reservation(self): return self.rental_history['active']
    def get_inactive_reservations(self): return self.rental_history['inactive']

    # Setters
    def set_vin(self, vin): self.vin = vin
    def set_model(self, model): self.model = model
    def set_base_rate(self, base_rate): self.base_rate = base_rate
    def set_img_url(self, img_url): self.img_url = img_url
    def set_seating_capacity(self, seating_capacity): self.seating_capacity = seating_capacity
    def set_colour(self, colour): self.colour = colour
    def set_car_type(self, car_type): self.car_type = car_type
    def set_features(self, features): self.features = features
    def set_rental_history(self, status, reservation_id):
        if status == 'active':
            self.rental_history['active'].append(reservation_id)
        elif status == 'inactive':
            self.rental_history['inactive'].append(reservation_id)
        elif status == 'delete':
            self.rental_history['active'].remove(reservation_id)
    
    def delete_reservation(self, reservation_id):
        if reservation_id in self.rental_history['active']:
            self.rental_history['active'].remove(reservation_id)
        elif reservation_id in self.rental_history['inactive']:
            self.rental_history['inactive'].remove(reservation_id)

    @abstractmethod
    def calculate_rental_cost(self, days):
        pass

    def to_dict(self):
        return {
            'vin': self.vin,
            'model': self.model,
            'base_rate': self.base_rate,
            'img_url': self.img_url,
            'seating_capacity': self.seating_capacity,
            'colour': self.colour,
            'car_type': self.car_type,
            'features': self.features,
            'category': self.__class__.__name__,
            'rental_history': self.rental_history
        }


class EconomyCar(Car):
    def __init__(self, vin, model, base_rate, img_url, seating_capacity, colour, car_type, features, fuel_efficiency, rental_history={'active': None, 'inactive': []}):
        super().__init__(vin, model, base_rate, img_url, seating_capacity, colour, car_type, features, rental_history)
        self.fuel_efficiency = fuel_efficiency

    def calculate_rental_cost(self, days):
        return (self.base_rate + (self.fuel_efficiency * 10)) * days

    def get_fuel_efficiency(self): return self.fuel_efficiency
    def set_fuel_efficiency(self, fuel_efficiency): self.fuel_efficiency = fuel_efficiency

    def to_dict(self):
        return super().to_dict() | {'fuel_efficiency': self.fuel_efficiency}

    @classmethod
    def from_dict(cls, data):
        return cls(
            vin=data['vin'],
            model=data['model'],
            base_rate=data['base_rate'],
            img_url=data['img_url'],
            seating_capacity=data['seating_capacity'],
            colour=data['colour'],
            car_type=data['car_type'],
            features=data['features'],
            fuel_efficiency=data['fuel_efficiency'],
            rental_history=data['rental_history']
        )


class LuxuryCar(Car):
    def __init__(self, vin, model, base_rate, img_url, seating_capacity, colour, car_type, features, chauffeur_available, rental_history={'active': None, 'inactive': []}):
        super().__init__(vin, model, base_rate, img_url, seating_capacity, colour, car_type, features, rental_history)
        self.chauffeur_available = chauffeur_available

    def calculate_rental_cost(self, days):
        return (self.base_rate + (int(self.chauffeur_available) * 3000)) * days

    def get_chauffeur_available(self): return self.chauffeur_available
    def set_chauffeur_available(self, chauffeur_available): self.chauffeur_available = chauffeur_available

    def to_dict(self):
        return super().to_dict() | {'chauffeur_available': self.chauffeur_available}

    @classmethod
    def from_dict(cls, data):
        return cls(
            vin=data['vin'],
            model=data['model'],
            base_rate=data['base_rate'],
            img_url=data['img_url'],
            seating_capacity=data['seating_capacity'],
            colour=data['colour'],
            car_type=data['car_type'],
            features=data['features'],
            chauffeur_available=data['chauffeur_available'],
            rental_history=data['rental_history']
        )


class CommercialCar(Car):
    def __init__(self, vin, model, base_rate, img_url, seating_capacity, colour, car_type, features, cargo_capacity, rental_history={'active': None, 'inactive': []}):
        super().__init__(vin, model, base_rate, img_url, seating_capacity, colour, car_type, features, rental_history)
        self.cargo_capacity = cargo_capacity

    def calculate_rental_cost(self, days):
        return (self.base_rate * days) + (self.cargo_capacity * 10)

    def get_cargo_capacity(self): return self.cargo_capacity
    def set_cargo_capacity(self, cargo_capacity): self.cargo_capacity = cargo_capacity

    def to_dict(self):
        return super().to_dict() | {'cargo_capacity': self.cargo_capacity}

    @classmethod
    def from_dict(cls, data):
        return cls(
            vin=data['vin'],
            model=data['model'],
            base_rate=data['base_rate'],
            img_url=data['img_url'],
            seating_capacity=data['seating_capacity'],
            colour=data['colour'],
            car_type=data['car_type'],
            features=data['features'],
            cargo_capacity=data['cargo_capacity'],
            rental_history=data['rental_history']
        )


# Mapping of car categories to classes    
CAR_CLASS_MAP = {
    "EconomyCar": EconomyCar,
    "LuxuryCar": LuxuryCar,
    "CommercialCar": CommercialCar
}
