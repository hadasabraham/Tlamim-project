class Form(object):

    def __init__(self, stage: int, form_id: str, form_link: str):
        self.id = form_id
        self.link = form_link
        self.stage = stage

    @staticmethod
    def get_attributes_info():
        info = [('stage_index', 'שלב', 'int'),
                ('form_id', 'מזהה', 'str'),
                ('form_link', 'קישור', 'str')]
        return info
