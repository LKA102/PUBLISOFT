from common.event import Event

class UserCreatedEvent(Event):
    def __init__(self, user_id, user_code=None, email=None, name=None, last_name=None):
        self.user_id = user_id
        self.name = name
        self.last_name = last_name