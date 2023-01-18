import numpy as np


class Candidate(object):

    def __init__(self, email: str, first_name: str, last_name: str, stage_index: int = 0, status: str = None):
        self.email = email.strip()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.stage_index = stage_index
        self.status = status.strip() if status is not None and status.strip().lower() != 'nan' and status.strip().lower() != 'null' else None

    def __str__(self):
        if self.status:
            res = f"(\'{self.email}\', \'{self.first_name}\', \'{self.last_name}\', {self.stage_index}, \'{self.status}\')"
        else:
            res = f"(\'{self.email}\', \'{self.first_name}\', \'{self.last_name}\', {self.stage_index}, NULL)"
        return res

    def to_json_list(self) -> list[dict]:
        name = self.first_name + " " + self.last_name
        stage = self.stage_index
        d = dict()
        d['email'] = self.email
        d['name'] = name
        d['stage'] = stage
        d['status'] = self.status if self.status is not None else ''
        return [d]

