from common.command import Command

class CreateRankingCommand(Command):
    def __init__(self, student_id, score, created_at):
        self.student_id = student_id
        self.score = score
        self.created_at = created_at