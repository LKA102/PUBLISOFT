from common.event import Event

class AdminUpdatedEvent(Event):
    def __init__(self, admin_id):
        self.admin_id = admin_id

class AdminDeletedEvent(Event):
    def __init__(self, admin_id):
        self.admin_id = admin_id

class RemoceStudentAccountEvent(Event):
    def __init__(self, student_id):
        self.student_id = student_id