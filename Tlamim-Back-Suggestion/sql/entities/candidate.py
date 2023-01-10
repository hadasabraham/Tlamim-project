class Candidate(object):

    def __init__(self, email: str, first_name: str, last_name: str, stage_index: int = 0, current_status: str = ''):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.stage_index = stage_index
        self.status = current_status

    @staticmethod
    def get_attributes_info():
        info = [('email', 'דואל', 'str'),
                ('fist_name', 'שם פרטי', 'str'),
                ('last_name', 'שם משפחה', 'str'),
                ('stage_index', 'שלב', 'int'),
                ('current_status', 'סטטוס', 'str')]
        return info

