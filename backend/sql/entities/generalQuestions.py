import os

import pandas as pd


class GeneralQuestions(object):

    def __init__(self, stage_index: int, file_path: str, file_type: str):
        file_path = file_path.strip()
        file_type = file_type.strip()

        self.stage_index = stage_index
        self.file_path = file_path.strip()
        self.file_type = file_type.strip()

        file_name = file_path.split(f"{os.path.sep}")[-1]
        header = fr"{os.getcwd()}{os.path.sep}backend{os.path.sep}sql{os.path.sep}data{os.path.sep}generalQuestions"
        path = fr"{header}{os.path.sep}{file_type}{os.path.sep}{file_name}"
        if not os.path.exists(path):
            if file_type == "xlsx":
                pd.read_excel(file_path).to_excel(path, index=False)
            else:
                pd.read_csv(file_path).to_csv(path, index=False)

        self.file_path = path


    def __str__(self):
        res = "(" + f"{self.stage_index}" + f", \'{self.file_path}\'" + f", \'{self.file_type}\')"
        return res


