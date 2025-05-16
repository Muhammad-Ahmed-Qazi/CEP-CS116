from datetime import datetime as dt

class Reservation:
    def __init__(self, id, user, car, start_date, end_date, cost, created_at=dt.now(), status='active'):
        self.id = id
        self.user = user
        self.car = car
        self.start_date = start_date
        self.end_date = end_date
        self.cost = cost
        self.status = status
        self.created_at = created_at
    
    # Getters
    def get_id(self):
        return self.id
    def get_user(self):
        return self.user
    def get_car(self):
        return self.car
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
    
    # Setters
    def set_id(self, id):
        self.id = id
    def set_user(self, user):
        self.user = user
    def set_car(self, car):
        self.car = car
    def set_start_date(self, start_date):
        self.start_date = start_date
    def set_end_date(self, end_date):
        self.end_date = end_date
    def set_cost(self, cost):
        self.cost = cost
    def set_status(self, status):
        self.status = status
    
    # Methods
    def to_dict(self):
        return {self.get_id(): {
            'id': self.get_id(),
            'user': self.get_user().get_email(),
            'car': self.get_car().get_vin(),
            'start_date': self.get_start_date().strftime('%Y-%m-%d'),
            'end_date': self.get_end_date().strftime('%Y-%m-%d'),
            'cost': self.get_cost(),
            'status': self.get_status(),
            'created_at': self.get_created_at().strftime('%Y-%m-%d %H:%M:%S')
        }}

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            user=data['user'],
            car=data['car'],
            start_date=dt.strptime(data['start_date'], '%Y-%m-%d'),
            end_date=dt.strptime(data['end_date'], '%Y-%m-%d'),
            cost=data['cost'],
            status=data['status'],
            created_at=dt.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
        )