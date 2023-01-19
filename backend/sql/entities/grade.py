class Grade(object):

    def __init__(self, email: str, stage_index: int, grade: float, passed: bool = None, notes: str = None):
        self.email = email.strip()
        self.stage_index = stage_index
        self.grade = grade
        self.passed = None if passed is None or 'nan' == str(passed).strip().lower() or 'null' == str \
            (passed).strip().lower() else passed
        self.notes = None if notes is None or 'nan' == str(notes).strip().lower() or 'null' == str \
            (notes).strip().lower() else notes.strip()

    def __str__(self):
        passed = self.passed if self.passed is not None else 'NULL'
        notes = f"\'{self.notes}\'" if self.notes is not None else 'NULL'
        res = "(" + f"\'{self.email}\'" + f", {self.stage_index}" + f", {self.grade}" + f", {passed}" + f", {notes})"
        return res

    def to_json_list(self) -> list[dict]:
        d = dict()
        d['grade'] = self.grade
        d['passed'] = ('True' if self.passed else 'False') if self.passed is not None else ''
        d['notes'] = self.notes if self.notes is not None and 'nan' != self.notes else ''
        return [d]

    def update_passed(self, passed: bool | None) -> bool:
        if passed is None:
            return False
        if self.passed is None:
            self.passed = passed
            return True
        else:
            if self.passed != passed:
                self.passed = passed
                return True
            else:
                return False

    def update_score(self, score: float | None) -> bool:
        if score is None:
            return False
        self.grade = self.grade if score is None else score
        return True

    def add_notes(self, notes: str | None) -> bool:
        if notes is None:
            return False
        if self.notes is None:
            self.notes = notes
        else:
            self.notes += "\r\n" + notes
        return True

