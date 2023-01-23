import os

import pandas as pd


class PrivateQuestions(object):

    def __init__(self, email: str, stage_index: int, table_path: str, file_type: str):
        self.email = email.strip()
        self.stage_index = stage_index
        self.table_path = table_path.strip()
        self.file_type = file_type.strip()

        file_name = self.table_path.split(f"{os.path.sep}")[-1]
        header = fr"{os.getcwd()}{os.path.sep}sql{os.path.sep}data{os.path.sep}privateQuestions"
        path = fr"{header}{os.path.sep}{file_type}{os.path.sep}{file_name}"
        if not os.path.exists(path):
            if file_type == "xlsx":
                pd.DataFrame().to_excel(path, index=False)
            else:
                pd.DataFrame().to_csv(path, index=False)

        if file_type == "xlsx":
            pd.read_excel(table_path).to_excel(path, index=False)
        else:
            pd.read_csv(table_path).to_csv(path, index=False)


        self.file_path = path

    def __str__(self):
        res = "(" + f"\'{self.email}\'" + f", {self.stage_index}" + f", \'{self.table_path}\'" + f", \'{self.file_type}\')"
        return res

