class CreateNotificationCommand:
    def __init__(self, title, message, type_, user_emisor_id, user_receptor_id):
        self.title = title
        self.message = message
        self.type = type_
        self.user_emisor_id = user_emisor_id
        self.user_receptor_id = user_receptor_id