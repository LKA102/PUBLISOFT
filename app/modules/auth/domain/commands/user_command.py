class RegisterUserCommand:
    def __init__(self, email, password, name, last_name):
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        # We invent (when creating the user entity) the usercode, ROLE is set to Student by default, State is Active by default