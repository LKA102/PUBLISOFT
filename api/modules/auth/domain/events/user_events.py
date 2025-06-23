class UserCreatedEvent:
    def __init__(self, user_id, user_code=None, email=None, name=None, last_name=None):
        self.user_id = user_id
        self.user_code = user_code
        self.email = email
        self.name = name
        self.last_name = last_name