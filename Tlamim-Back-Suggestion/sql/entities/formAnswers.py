
class FormAnswers(object):

    def __init__(self, email: str, form_id: str, row_index: int, timestamp: str):
        self.email = email.strip()
        self.form_id = form_id.strip()
        self.row_index = row_index
        self.timestamp = timestamp

    def __str__(self):
        res = "(" + f"\'{self.email}\'" + f", \'{self.form_id}\'" + f", {self.row_index}" + f", \'{self.timestamp}\')"
        return res
