class Candidate:

    def __init__(self, email: str, name: str, stage: int, status: str = ''):
        self.email = email
        self.name = name
        self.stage = stage
        self.status = status
