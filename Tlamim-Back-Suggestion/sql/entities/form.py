import os


class Form(object):

    def __init__(self, form_id: str, form_link: str, stage_index: int, responses_file_path: str = None, file_type: str = 'xlsx'):
        self.form_id = form_id.strip()
        self.form_link = form_link.strip()
        self.stage_index = stage_index
        if responses_file_path:
            self.responses_file_path = responses_file_path.strip()
        else:
            # if responses save path wasn't provided use the form id and save in the appropriate
            # folder according to type of file (i.e. xlsx\csv folder)
            header = os.getcwd().split("\\")[:-1]
            header = "\\".join(header)
            if file_type == 'xlsx':
                self.responses_file_path = fr"{header}\xlsx\{form_id}.xlsx"
            else:
                self.responses_file_path = fr"{header}\csv\{form_id}.csv"

        self.file_type = file_type.strip()

    def __str__(self):
        res = "(" + f"\'{self.form_id}\'" + f", \'{self.form_link}\'" + \
              f", {self.stage_index}" + f", \'{self.responses_file_path}\'" + f", \'{self.file_type}\')"
        return res
