from .form import Form


class Stage(object):

    def __init__(self, stage_index: int, stage_name: str):
        self.index = stage_index
        self.name = stage_name
        self.forms = []

    def add_form(self, form_id, form_link):
        self.forms.append(Form(stage=self.index, form_id=form_id, form_link=form_link))

    @staticmethod
    def get_attributes_info():
        info = [('stage_index', 'מספר שלב', 'int'),
                ('stage_name', 'שם שלב', 'str')]
        return info
