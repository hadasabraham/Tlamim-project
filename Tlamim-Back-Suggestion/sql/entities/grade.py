class Grade(object):

    def __init__(self, stage: int, grade: float, notes: list[str] = None, passed: bool = None):
        self.stage = stage
        self.grade = grade
        self.notes = notes
        self.passed = passed


    @staticmethod
    def get_attributes_info():
        info = [('stage_index', 'מספר שלב', 'int'),
                ('candidate_email', 'דואל', 'str'),
                ('grade', 'ציון', 'float'),
                ('notes', 'הערות', 'list[str]'),
                ('passed', 'עבר', 'bool')]
        return info

    def get_notes_str(self):
        res = ""
        if self.notes:
            for note in self.notes:
                res += note + ","
            return res[:-1]
        return res
