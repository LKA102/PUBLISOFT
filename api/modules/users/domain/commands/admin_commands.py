from common.command import Command
from uuid import UUID

class CreateAdminCommand(Command):
    def __init__(self, id: UUID, name: str, last_name: str):
        self.id = id
        self.name = name
        self.last_name = last_name

        
class UpdateAdminCommand(Command):
    def __init__(self, id: UUID, name: str, last_name: str, email: str, password: str, faculty: str):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.faculty = faculty
        
class DisableAdminCommand(Command):
    def __init__(self, id: UUID):
        self.id = id
        
class DisableStudentAccountCommand(Command):
    def __init__(self, admin_id: UUID, student_id: UUID):
        self.admin_id = admin_id
        self.student_id = student_id