from common.event import Event

class AdminUpdatedEvent(Event):
    def __init__(self, admin_id, email, password):
        self.admin_id = admin_id
        self.email = email
        self.password = password

class AdminDisabledEvent(Event):
    def __init__(self, admin_id):
        self.admin_id = admin_id

class DisableStudentAccountEvent(Event):
    def __init__(self, student_id):
        self.student_id = student_id