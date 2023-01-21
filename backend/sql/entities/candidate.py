import numpy as np


class Candidate(object):

    def __init__(self, email: str, first_name: str, last_name: str, stage_index: int = 0, status: str = None,
                 timestamp: str = None):
        self.email = email.strip()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.stage_index = stage_index
        self.status = status.strip() if status is not None and status.strip().lower() != 'nan' and status.strip().lower() != 'null' else None
        self.timestamp = timestamp.strip() if timestamp is not None and timestamp.strip().lower() != 'nan' and timestamp.strip().lower() != 'null' else None

    def __str__(self):
        first = self.first_name.replace('\'', '\'\'')
        last = self.last_name.replace('\'', '\'\'')
        timestamp = "\'\'" if self.timestamp is None else f"\'{self.timestamp}\'"
        if self.status:
            res = f"(\'{self.email}\', \'{first}\', \'{last}\', {self.stage_index}, \'{self.status}\'" + f", {timestamp})"
        else:
            res = f"(\'{self.email}\', \'{first}\', \'{last}\', {self.stage_index}, NULL" + f", {timestamp})"
        return res

    def to_json_list(self) -> list[dict]:
        name = self.first_name + " " + self.last_name
        stage = self.stage_index
        d = dict()
        d['email'] = self.email
        d['name'] = name
        d['stage'] = stage
        d['status'] = self.status if self.status is not None else ''
        d['timestamp'] = self.timestamp if self.timestamp is not None else ''
        return [d]
