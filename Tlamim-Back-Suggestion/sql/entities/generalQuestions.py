


class GeneralQuestions(object):

    def __init__(self, stage_index: int, file_path: str, file_type: str):
        self.stage_index = stage_index
        self.file_path = file_path
        self.file_type = file_type

    def __str__(self):
        res = "(" + f"{self.stage_index}" + f", \'{self.file_path}\'" + f", \'{self.file_type}\')"
        return res
