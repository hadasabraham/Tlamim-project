class Candidate(object):

    def __init__(self, email: str, first_name: str, last_name: str, stage_index: int = 0, status: str = None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.stage_index = stage_index
        self.status = status

    def __str__(self):
        if self.status:
            res = f"(\'{self.email}\', \'{self.first_name}\', \'{self.last_name}\', {self.stage_index}, \'{self.status}\')"
        else:
            res = f"(\'{self.email}\', \'{self.first_name}\', \'{self.last_name}\', {self.stage_index}, NULL)"
        return res

