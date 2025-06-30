from common.command import Command

class RegisterUserCommand(Command):
    def __init__(self, email, password, name, last_name, role):
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        self.role = role

class LoginUserCommand(Command):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
class UpdateUserCommand(Command):
    def __init__(self, user_id, email=None, password=None):
        self.user_id = user_id
        self.email = email
        self.password = password
        
class DisableUserCommand(Command):
    def __init__(self, user_id):
        self.user_id = user_id