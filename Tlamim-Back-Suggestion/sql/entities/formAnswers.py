
class FormAnswers(object):

    def __init__(self, email: str, form_id: str, row_index: int):
        self.email = email
        self.form_id = form_id
        self.row_index = row_index

    def __str__(self):
        res = "(" + f"\'{self.email}\'" + f", \'{self.form_id}\'" + f", {self.row_index})"
        return res
