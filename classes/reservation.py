from datetime import datetime as dt

class Reservation:
    def __init__(self, id, user_email, car_vin, start_date, end_date, cost, created_at=dt.now(), status='active', return_date=None):
        self.id = id
        self.user_email = user_email
        self.car_vin = car_vin
        self.start_date = start_date
        self.end_date = end_date
        self.cost = cost
        self.status = status
        self.created_at = created_at
        self.return_date = return_date  # ✅ New attribute

    # Getters
    def get_id(self):
        return self.id
    def get_user_email(self):
        return self.user_email
    def get_car_vin(self):
        return self.car_vin
    def get_start_date(self):
        return self.start_date
    def get_end_date(self):
        return self.end_date
    def get_cost(self):
        return self.cost
    def get_status(self):
        return self.status
    def get_created_at(self):
        return self.created_at
    def get_return_date(self):
        return self.return_date  # ✅ New

    # Setters
    def set_id(self, id):
        self.id = id
    def set_user_email(self, user_email):
        self.user_email = user_email
    def set_car_vin(self, car_vin):
        self.car_vin = car_vin
    def set_start_date(self, start_date):
        self.start_date = start_date
    def set_end_date(self, end_date):
        self.end_date = end_date
    def set_cost(self, cost):
        self.cost = cost
    def set_status(self, status):
        self.status = status
    def set_return_date(self, return_date):
        self.return_date = return_date  # ✅ New

    # Methods
    def to_dict(self):
        return {
            'id': self.get_id(),
            'user_email': self.get_user_email(),
            'car_vin': self.get_car_vin(),
            'start_date': self.get_start_date().strftime('%Y-%m-%d'),
            'end_date': self.get_end_date().strftime('%Y-%m-%d'),
            'cost': self.get_cost(),
            'status': self.get_status(),
            'created_at': self.get_created_at().strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': self.get_return_date().strftime('%Y-%m-%d') if self.get_return_date() else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            user_email=data['user_email'],
            car_vin=data['car_vin'],
            start_date=dt.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=dt.strptime(data['end_date'], '%Y-%m-%d').date(),
            cost=data['cost'],
            status=data['status'],
            created_at=dt.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S'),
            return_date=dt.strptime(data['return_date'], '%Y-%m-%d').date() if data.get('return_date') else None
        )
