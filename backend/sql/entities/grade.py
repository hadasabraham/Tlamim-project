class Grade(object):

    def __init__(self, email: str, stage_index: int, grade: float | None, passed: bool = None, notes: str = None,
                 timestamp: str = None):
        self.email = email.strip()
        self.stage_index = stage_index
        self.grade = grade
        self.passed = None if passed is None or 'nan' == str(passed).strip().lower() or 'null' == str \
            (passed).strip().lower() else passed
        self.notes = None if notes is None or 'nan' == str(notes).strip().lower() or 'null' == str \
            (notes).strip().lower() else notes.strip()
        self.timestamp = None if timestamp is None or 'nan' == str(timestamp).strip().lower() or 'null' == str \
            (timestamp).strip().lower() else timestamp.strip()

    def __str__(self):
        passed = self.passed if self.passed is not None else 'NULL'
        timestamp = "\'\'" if self.timestamp is None else f"\'{self.timestamp}\'"
        if self.notes is None:
            notes = 'NULL'
        else:
            notes = self.notes.replace('\'', '\'\'')
        res = "(" + f"\'{self.email}\'" + f", {self.stage_index}" + f", {self.grade}" + f", {passed}" + f", \'{notes}\'" + f", {timestamp})"
        return res

    def to_json_list(self) -> list[dict]:
        d = dict()
        d['grade'] = self.grade
        d['passed'] = ('True' if self.passed else 'False') if self.passed is not None else ''
        d['notes'] = self.notes if self.notes is not None and 'nan' != self.notes else ''
        d['timestamp'] = self.timestamp if self.timestamp is not None and 'nan' != self.timestamp else ''
        return [d]

    def update_timestamp(self, timestamp: str):
        self.timestamp = timestamp


    def update_passed(self, passed: bool | None) -> bool:
        if passed is None:
            return False
        if self.passed is None:
            self.passed = passed
            return True
        if self.passed != passed:
            self.passed = passed
            return True
        return False

    def update_score(self, score: float | None) -> bool:
        if score is None:
            return False
        self.grade = self.grade if score is None else score
        return True

    def update_notes(self, notes: str | None) -> bool:
        if notes is None:
            return False
        self.notes = notes.strip().replace('\'', '\'\'')
        return True
