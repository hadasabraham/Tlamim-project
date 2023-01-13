import numpy as np
import pandas as pd


class Table(object):

    def __init__(self, path: str, table_type: str, hebrew_table: bool):
        self.table = pd.read_csv(path.strip()) if table_type.strip() == 'csv' else pd.read_excel(path)
        self.hebrew_table = hebrew_table

    @staticmethod
    def find_row(path: str, file_type: str, english_key: str, hebrew_key: str, value):
        table = pd.read_csv(path.strip()) if file_type.strip() == 'csv' else pd.read_excel(path)
        if english_key in table.columns.tolist():
            row = table[table[english_key] == value]
        elif hebrew_key in table.columns.tolist():
            row = table[table[hebrew_key] == value]
        else:
            return None
        return row

    @staticmethod
    def get_row(path: str, file_type: str, row_index: int):
        if file_type.strip() == 'csv':
            row = pd.read_csv(path, skiprows=lambda x: x not in [row_index, 0])
        else:
            row = pd.read_excel(path, skiprows=lambda x: x not in [row_index, 0])
        return row

    @staticmethod
    def row_to_json_list(row: pd.DataFrame, english_key: str = "email", hebrew_key: str = 'דוא"ל', include_key=True):
        answers = []
        for question in row.columns.tolist():
            ans = dict()
            if not include_key and (str(question) == english_key or str(question) == hebrew_key):
                continue
            ans['title'] = str(question)
            ans['answer'] = row[question][row.index[0]]
            answers.append(ans)
        return answers

    @staticmethod
    def get_row_as_json_list(path: str, file_type: str, row_index: int):
        row = Table.get_row(path=path, file_type=file_type, row_index=row_index)
        return Table.row_to_json_list(row=row)

    @staticmethod
    def get_sql_cols():
        pass

    def get_cols(self):
        cols = []
        for col in self.table.columns.tolist():
            if 'Unnamed' in col:
                continue
            cols.append(col)

        return cols

    def get_rows_to_load(self, sql_columns: list[tuple[str, str]]) -> list[str]:
        rows = []

        for col_eng_name, col_type, col_heb_name in sql_columns:
            col_name = col_heb_name if self.hebrew_table else col_eng_name
            if col_name not in self.table.columns.tolist():
                # filling necessary columns with default values
                if col_type == 'str':
                    col_values = pd.Series(['' for _ in range(len(self.table.index))])
                elif col_type == 'bool':
                    col_values = pd.Series(['NULL' for _ in range(len(self.table.index))])
                else:
                    col_values = pd.Series([0 for _ in range(len(self.table.index))])

                self.table[col_name] = col_values

        for _, table_row in self.table.iterrows():
            entry = []
            for col_eng_name, col_type, col_heb_name in sql_columns:
                col_name = col_heb_name if self.hebrew_table else col_eng_name
                if str(table_row[col_name]).lower() == 'null' or table_row[col_name] is np.nan or 'nan' == str(table_row[col_name]).lower():
                    # nullable property
                    val = "NULL"
                elif col_type == 'str':
                    v = str(table_row[col_name]).replace("\'", "\'\'")
                    val = f"\'{v}\'"
                elif col_type == 'int':
                    val = f"{table_row[col_name]}"
                elif col_type == 'bool':
                    v = 1 if table_row[col_name] == 1 else 0
                    val = f"{v}"
                elif col_type == 'float':
                    val = f"{table_row[col_name]}"
                else:
                    continue
                entry.append(val)
            rows.append(','.join(entry))
        return rows


class StagesTable(Table):

    def __init__(self, path: str, table_type: str, hebrew_table: bool):
        super().__init__(path, table_type, hebrew_table)

    @staticmethod
    def get_sql_cols():
        return [("stage_index", "int", "מספר שלב"), ("stage_name", "str", "שם שלב")]


class CandidatesTable(Table):

    def __init__(self, path: str, table_type: str, hebrew_table: bool):
        super().__init__(path, table_type, hebrew_table)

    @staticmethod
    def get_sql_cols():
        return [("email", "str", 'דוא"ל'), ("first_name", "str", "שם פרטי"), ("last_name", "str", "שם משפחה"),
                ("stage_index", "int", "מספר שלב"),
                ("status", "str", "סטטוס תהליך")]


class GeneralQuestionsTable(Table):

    def __init__(self, path: str, table_type: str, hebrew_table: bool):
        super().__init__(path, table_type, hebrew_table)

    @staticmethod
    def get_sql_cols():
        return [("stage_index", "int", "מספר שלב"), ("file_path", "str", "מיקום קובץ"),
                ("file_type", "str", "סוג קובץ")]


class FormsTable(Table):

    def __init__(self, path: str, table_type: str, hebrew_table: bool):
        super().__init__(path, table_type, hebrew_table)

    @staticmethod
    def get_sql_cols():
        return [("form_id", "str", "מזהה"), ("form_link", "str", "קישור"), ("stage_index", "int", "מספר שלב"),
                ("responses_file_path", "str", "מיקום קובץ תשובות"),
                ("file_type", "str", "סוג קובץ")]


class FormsAnswersTable(Table):

    def __init__(self, path: str, table_type: str, hebrew_table: bool):
        super().__init__(path, table_type, hebrew_table)

    @staticmethod
    def get_sql_cols():
        return [("email", "str", 'דוא"ל'), ("form_id", "str", "מזהה"), ("row_index", "int", "שורה")]


class PrivateQuestionsTable(Table):

    def __init__(self, path: str, table_type: str, hebrew_table: bool):
        super().__init__(path, table_type, hebrew_table)

    @staticmethod
    def get_sql_cols():
        return [("email", "str", 'דוא"ל'), ("stage_index", "int", "מספר שלב"), ("table_path", "str", "מיקום קובץ"),
                ("file_type", "str", "סוג קובץ")]


class GradesTable(Table):

    def __init__(self, path: str, table_type: str, hebrew_table: bool):
        super().__init__(path, table_type, hebrew_table)

    @staticmethod
    def get_sql_cols():
        return [("email", "str", 'דוא"ל'), ("stage_index", "int", "מספר שלב"), ("grade", "float", "ציון"),
                ("passed", "bool", "עבר/ לא עבר"), ("notes", "str", "הערות")]
