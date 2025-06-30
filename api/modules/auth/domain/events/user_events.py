from common.event import Event

class UserCreatedEvent(Event):
    def __init__(self, user_id, name, last_name, role):
        self.user_id = user_id
        self.name = name
        self.last_name = last_name
        self.role = role