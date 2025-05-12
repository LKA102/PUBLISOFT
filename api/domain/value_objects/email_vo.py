class EmailVO:
    def __init__(self, email: str):
        if "@" not in email:
            raise ValueError("Invalid email format")
        self.email = email

    def __str__(self):
        return self.email