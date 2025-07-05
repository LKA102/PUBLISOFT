from common.command import Command
from uuid import UUID

class CreateStudentCommand(Command):
    def __init__(self, id: UUID, name: str, last_name: str):
        self.id = id
        self.name = name
        self.last_name = last_name

class UpdateStudentCommand(Command):
    def __init__(self, id: UUID, name: str, last_name: str, email: str, password: str, faculty: str, career: str):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.faculty = faculty
        self.career = career

class DisableStudentCommand(Command):
    def __init__(self, id: UUID):
        self.id = id