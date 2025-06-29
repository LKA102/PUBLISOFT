from common.event import Event

class StudentUpdatedEvent(Event):
    def __init__(self, student_id, email, password):
        self.student_id = student_id
        self.email = email
        self.password = password

class StudentDisabledEvent(Event):
    def __init__(self, student_id):
        self.student_id = student_id