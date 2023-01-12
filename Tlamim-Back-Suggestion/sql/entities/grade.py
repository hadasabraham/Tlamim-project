class Grade(object):

    def __init__(self, email: str, stage_index: int, grade: float, passed: bool = None, notes: str = None):
        self.email = email
        self.stage_index = stage_index
        self.grade = grade
        self.passed = passed
        self.notes = notes

    def __str__(self):
        passed = self.passed if self.passed else 'NULL'
        notes = f"\'{self.notes}\'" if self.passed else 'NULL'
        res = "(" + f"\'{self.email}\'" + f", {self.stage_index}" + f", {self.grade}" + f", {passed}" + f", {notes})"
        return res
