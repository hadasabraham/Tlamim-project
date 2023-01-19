import os

import pandas as pd


class Form(object):

    def __init__(self, form_id: str, form_link: str, stage_index: int, responses_file_path: str = None, file_type: str = 'xlsx'):
        self.form_id = form_id.strip()
        self.form_link = form_link.strip()
        self.stage_index = stage_index
        header = os.getcwd().split(f"{os.path.sep}")
        path = f"{os.path.sep}".join(header) + f"{os.path.sep}sql{os.path.sep}data{os.path.sep}formsAnswers{os.path.sep}{file_type.strip()}"

        if responses_file_path:
            file_name = responses_file_path.strip().split(f"{os.path.sep}")[-1]
            path = fr"{path}{os.path.sep}{file_name}"
            self.responses_file_path = path
            if file_type.strip() == 'xlsx':
                data = pd.read_excel(responses_file_path.strip())
                data.to_excel(path, index=False)
            else:
                data = pd.read_csv(responses_file_path.strip())
                data.to_csv(path, index=False)

        else:
            # if responses save path wasn't provided use the form id and save in the appropriate
            # folder according to type of file (i.e. xlsx\csv folder)
            if file_type.strip() == 'xlsx':
                self.responses_file_path = fr"{path}{os.path.sep}{form_id}.xlsx"
                if not os.path.exists(self.responses_file_path):
                    pd.DataFrame().to_excel(self.responses_file_path, index=False)
            else:
                self.responses_file_path = fr"{path}{os.path.sep}{form_id}.csv"
                if not os.path.exists(self.responses_file_path):
                    pd.DataFrame().ro_csv(self.responses_file_path, index=False)

        self.file_type = file_type.strip()

    def __str__(self):
        res = "(" + f"\'{self.form_id}\'" + f", \'{self.form_link}\'" + \
              f", {self.stage_index}" + f", \'{self.responses_file_path}\'" + f", \'{self.file_type}\')"
        return res
