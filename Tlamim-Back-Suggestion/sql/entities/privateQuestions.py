

class PrivateQuestions(object):

    def __init__(self, email: str, stage_index: int, table_path: str, file_type: str):
        self.email = email.strip()
        self.stage_index = stage_index
        self.table_path = table_path.strip()
        self.file_type = file_type.strip()

    def __str__(self):
        res = "(" + f"\'{self.email}\'" + f", {self.stage_index}" + f", \'{self.table_path}\'" + f", \'{self.file_type}\')"
        return res

