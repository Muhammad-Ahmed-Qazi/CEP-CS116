from abc import ABC, abstractmethod

class Car(ABC):
    def __init__(self, vin, make, model, year, mileage, colour, car_type, category, is_available, base_rate, features):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.colour = colour
        self.car_type = car_type
        self.category = category
        self.is_available = is_available
        self.base_rate = base_rate
        self.features = features
        self.rental_history = []
    
    # Getters
    def get_vin(self):
        return self.vin
    def get_make(self):
        return self.make
    def get_model(self):
        return self.model
    def get_year(self):
        return self.year
    def get_mileage(self):
        return self.mileage
    def get_colour(self):
        return self.colour
    def get_car_type(self):
        return self.car_type
    def get_category(self):
        return self.category
    def get_is_available(self):
        return self.is_available
    def get_base_rate(self):
        return self.base_rate
    def get_features(self):
        return self.features
    def get_rental_history(self):
        return self.rental_history

    # Setters
    def set_vin(self, vin):
        self.vin = vin
    def set_make(self, make):
        self.make = make
    def set_model(self, model):
        self.model = model
    def set_year(self, year):
        self.year = year
    def set_mileage(self, mileage):
        self.mileage = mileage
    def set_colour(self, colour):
        self.colour = colour
    def set_car_type(self, car_type):
        self.car_type = car_type
    def set_category(self, category):
        self.category = category
    def set_is_available(self, is_available):
        self.is_available = is_available
    def set_base_rate(self, base_rate):
        self.base_rate = base_rate
    def set_features(self, features):
        self.features = features
    def set_rental_history(self, reservation):
        self.rental_history.append(reservation)
    
    @abstractmethod
    def calculate_rental_cost(self, rental_period):
        pass

class EconomyCar(Car):
    def __init__(self, vin, make, model, year, mileage, colour, category, is_available, base_rate, features):
        super().__init__(vin, make, model, year, mileage, colour, "Economy", category, is_available, base_rate, features)

    def calculate_rental_cost(self, rental_period):
        return (self.base_rate + (self.features['fuel_efficiency'] * 30)) * rental_period
    
    @classmethod
    def from_json(cls, data):
        obj = EconomyCar(data['vin'], data['make'], data['model'], data['year'], data['mileage'], data['colour'], data['car_type'], data['category'], data['is_available'], data['base_rate'], data['features'])
        obj.rental_history = data['rental_history']
        return obj

class LuxuryCar(Car):
    def __init__(self, vin, make, model, year, mileage, colour, category, is_available, base_rate, features, chauffeur_available):
        super().__init__(vin, make, model, year, mileage, colour, "Luxury", category, is_available, base_rate, features)
        self.chauffeur_available = chauffeur_available

    # Getters and Setters for chauffeur_available
    def get_chauffeur_available(self):
        return self.chauffeur_available

    def set_chauffeur_available(self, chauffeur_available):
        self.chauffeur_available = chauffeur_available

    def calculate_rental_cost(self, rental_period):
        return (self.base_rate + (int(self.chauffeur_available) * 1500) + (self.features['fuel_efficiency'] * 30)) * rental_period
    
    @classmethod
    def from_json(cls, data):
        obj = LuxuryCar(data['vin'], data['make'], data['model'], data['year'], data['mileage'], data['colour'], data['car_type'], data['category'], data['is_available'], data['base_rate'], data['features'])
        obj.rental_history = data['rental_history']
        obj.chauffeur_available = data['chauffeur_available']
        return obj

class CommercialCar(Car):
    def __init__(self, vin, make, model, year, mileage, colour, category, is_available, base_rate, features, load_capacity):
        super().__init__(vin, make, model, year, mileage, colour, "Commercial", category, is_available, base_rate, features)
        self.load_capacity = load_capacity

    # Getters and Setters for load_capacity
    def get_load_capacity(self):
        return self.load_capacity

    def set_load_capacity(self, load_capacity):
        self.load_capacity = load_capacity

    def calculate_rental_cost(self, rental_period):
        return (self.base_rate + (self.features['fuel_efficiency'] * 30) + (self.load_capacity * 10)) * rental_period
    
    @classmethod
    def from_json(cls, data):
        obj = Car(data['vin'], data['make'], data['model'], data['year'], data['mileage'], data['colour'], data['car_type'], data['category'], data['is_available'], data['base_rate'], data['features'])
        obj.rental_history = data['rental_history']
        obj.load_capacity = data['load_capacity']
        return obj