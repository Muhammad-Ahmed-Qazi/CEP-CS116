from helpers.file_handler import FileHandler
from classes.car import CAR_CLASS_MAP

class Fleet:

    file_handler = FileHandler()

    def __init__(self):
        self.cars = self.load_cars()
    
    # Getters
    def get_cars(self):
        return self.cars
    def get_car_by_vin(self, vin):
        for car in self.cars:
            if car.get_vin() == vin:
                return car
        return None
    
    # Setters
    # def set_car_by_vin(self, vin, car):
    #     for i, c in enumerate(self.cars):
    #         if c.get_vin() == vin:
    #             self.cars[i] = car
    #             return True
    #     return False

    # Methods
    def add_car(self, car):
        if not self.get_cars():
            self.cars = [car]
        else:
            for existing_car in self.cars:
                if existing_car.get_vin() == car.get_vin():
                    print(f"Car with VIN {car.get_vin()} already exists.") # Raise custom exceptions!
                    return False
            self.cars.append(car)
    
    def remove_car(self, vin):
        car = self.get_car_by_vin(vin)
        if car:
            self.cars.remove(car)
            return True
        return False
    
    def load_cars(self):
        car_dicts = Fleet.file_handler.load_data('cars')
        if not car_dicts:
            self.cars = []
            return

        car_objects = []
        for data in car_dicts:
            category = data.get("category")
            car_class = CAR_CLASS_MAP.get(category)
            if car_class:
                car_objects.append(car_class.from_dict(data))
            else:
                print(f"Unknown car category '{category}' in data: {data['vin']}")
        
        return car_objects
    
    def save_cars(self):
        car_dicts = [car.to_dict() for car in self.cars]
        Fleet.file_handler.save_data('cars', car_dicts)