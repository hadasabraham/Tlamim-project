import os
import sqlite3 as sql

import pandas as pd

from entities.stage import Stage
from entities.form import Form
from entities.candidate import Candidate
from entities.grade import Grade
from entities.generalQuestions import GeneralQuestions
from entities.formAnswers import FormAnswers
from entities.privateQuestions import PrivateQuestions
from entities.table import *


class SqlServer(object):

    def __init__(self, database='test_database'):
        self.__conn = sql.connect(database=database)

    def create_tables(self):
        curser = self.__conn.cursor()

        query = "CREATE TABLE IF NOT EXISTS Stages(stage_index INTEGER PRIMARY KEY, stage_name TEXT NOT NULL, CHECK(stage_index >= 0));"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS Candidates(email TEXT PRIMARY KEY, first_name TEXT NOT NULL, " \
                "last_name NOT NULL, stage_index INTEGER, status TEXT, " \
                " FOREIGN KEY(stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS GeneralQuestions(stage_index INTEGER PRIMARY KEY, " \
                "file_path TEXT NOT NULL, file_type TEXT NOT NULL, CHECK(file_type IN ('csv', 'xlsx')), " \
                "FOREIGN KEY(stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS Forms(form_id TEXT PRIMARY KEY, " \
                "form_link TEXT NOT NULL, stage_index INTEGER, responses_file_path TEXT NOT NULL, " \
                "file_type TEXT NOT NULL, CHECK(file_type IN ('csv', 'xlsx')), " \
                " FOREIGN KEY(stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS FormsAnswers(email TEXT, form_id TEXT, row_index INTEGER NOT NULL, timestamp TEXT NOT NULL, " \
                "CHECK(row_index >= 1), PRIMARY KEY(email, form_id), " \
                "FOREIGN KEY(email) REFERENCES Candidates(email) ON DELETE CASCADE, " \
                "FOREIGN KEY(form_id) REFERENCES Forms(form_id) ON DELETE CASCADE);"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS PrivateQuestions(email TEXT, stage_index TEXT, table_path TEXT NOT NULL, file_type TEXT NOT NULL, " \
                "PRIMARY KEY(email, stage_index), CHECK(file_type IN ('csv', 'xlsx')), " \
                "FOREIGN KEY(email) REFERENCES Candidates(email) ON DELETE CASCADE, " \
                "FOREIGN KEY(stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS Grades(email TEXT, stage_index INTEGER, " \
                "grade FLOAT NOT NULL, passed BOOL, notes TEXT, PRIMARY KEY(email, stage_index), " \
                "FOREIGN KEY(email) REFERENCES Candidates(email) ON DELETE CASCADE, " \
                "FOREIGN KEY(stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        self.__conn.commit()

    def drop_tables(self):
        curser = self.__conn.cursor()

        query = "DROP TABLE IF EXISTS Grades;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS PrivateQuestions;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS FormsAnswers;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS Forms;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS GeneralQuestions;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS Candidates;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS Stages;"
        curser.execute(query)

        self.__conn.commit()

    def clear_tables(self):
        curser = self.__conn.cursor()

        query = "DELETE FROM Grades;"
        curser.execute(query)

        query = "DELETE FROM PrivateQuestions;"
        curser.execute(query)

        query = "DELETE FROM FormsAnswers;"
        curser.execute(query)

        query = "DELETE FROM Forms;"
        curser.execute(query)

        query = "DELETE FROM GeneralQuestions;"
        curser.execute(query)

        query = "DELETE FROM Candidates;"
        curser.execute(query)

        query = "DELETE FROM Stages;"
        curser.execute(query)

        self.__conn.commit()

    def add_stage(self, stage: Stage):
        curser = self.__conn.cursor()
        query = "INSERT INTO Stages(stage_index, stage_name) VALUES {0};".format(str(stage))
        curser.execute(query)
        self.__conn.commit()

    def get_stagesTable(self) -> pd.DataFrame:
        curser = self.__conn.cursor()
        query = "SELECT * FROM Stages ORDER BY stage_index ASC;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in StagesTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_stagesTable(self, path: str, file_type: str, hebrew_table: bool):
        table = StagesTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=StagesTable.get_sql_cols()):
            query = "INSERT INTO Stages(stage_index, stage_name) VALUES ({0});".format(row)
            curser.execute(query)
        self.__conn.commit()

    def export_stagesTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        stages_table = self.get_stagesTable()
        if hebrew_table:
            stages_table.columns = [heb for _, _, heb in StagesTable.get_sql_cols()]

        if file_type == 'csv':
            stages_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            stages_table.to_excel(path, index=index)

    def add_grade(self, grade: Grade):
        curser = self.__conn.cursor()
        query = "INSERT INTO Grades(email, stage_index, grade, passed, notes) VALUES {0};".format(str(grade))
        curser.execute(query)
        self.__conn.commit()

    def get_gradesTable(self) -> pd.DataFrame:
        curser = self.__conn.cursor()
        query = "SELECT * FROM Grades;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in GradesTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_gradesTable(self, path: str, file_type: str, hebrew_table: bool = False):
        table = GradesTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=GradesTable.get_sql_cols()):
            query = "INSERT INTO Grades(email, stage_index, grade, passed, notes) VALUES ({0});".format(row)
            curser.execute(query)
        self.__conn.commit()

    def export_gradesTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        grades_table = self.get_gradesTable()
        if hebrew_table:
            grades_table.columns = [heb for _, _, heb in GradesTable.get_sql_cols()]
        if file_type == 'csv':
            grades_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            grades_table.to_excel(path, index=index)

    def add_privateQuestions(self, private_questions: PrivateQuestions):
        curser = self.__conn.cursor()
        query = "INSERT INTO PrivateQuestions(email, stage_index, table_path, file_type) VALUES {0};".format(
            str(private_questions))
        curser.execute(query)
        self.__conn.commit()

    def _get_privateQuestionsTable(self) -> pd.DataFrame:
        curser = self.__conn.cursor()
        query = "SELECT * FROM PrivateQuestions;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in PrivateQuestionsTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_privateQuestionsTable(self, path: str, file_type: str, hebrew_table: bool = False):
        table = PrivateQuestionsTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        SqlServer.refresh_privateQuestionsTablePaths(table=table, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=PrivateQuestionsTable.get_sql_cols()):
            query = "INSERT INTO PrivateQuestions(email, stage_index, table_path, file_type) VALUES ({0});".format(row)
            curser.execute(query)
        self.__conn.commit()

    @staticmethod
    def refresh_privateQuestionsTablePaths(table: PrivateQuestionsTable, hebrew_table=False):
        header = fr"{os.getcwd()}\data\privateQuestions"
        file_path = "table_path" if not hebrew_table else "מיקום קובץ"
        file_type = "file_type" if not hebrew_table else "סוג קובץ"
        columns = table.get_cols()
        refreshed = []
        for _, row in table.table.iterrows():
            refreshed_row = []
            for col in columns:
                if col == file_path:
                    path = "{0}\\{1}\\{2}".format(header, row[file_type], row[file_path].split('\\')[-1])
                    refreshed_row.append(path)
                else:
                    refreshed_row.append(row[col])
            refreshed.append(refreshed_row)
        refreshed_table = pd.DataFrame(refreshed, columns=columns)
        table.table = refreshed_table

    def export_privateQuestionsTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        private_questions_table = self._get_privateQuestionsTable()
        if hebrew_table:
            private_questions_table.columns = [heb for _, _, heb in PrivateQuestionsTable.get_sql_cols()]
        if file_type == 'csv':
            private_questions_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            private_questions_table.to_excel(path, index=index)

    def add_form(self, form: Form):
        curser = self.__conn.cursor()
        query = "INSERT INTO Forms(form_id, form_link, stage_index, responses_file_path, file_type) VALUES {0};".format(
            str(form))
        curser.execute(query)
        self.__conn.commit()

    def _get_formsTable(self) -> pd.DataFrame:
        curser = self.__conn.cursor()
        query = "SELECT * FROM Forms;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in FormsTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_formsTable(self, path: str, file_type: str, hebrew_table: bool = False):
        table = FormsTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        SqlServer.refresh_formsTablePaths(table=table, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=FormsTable.get_sql_cols()):
            query = "INSERT INTO Forms(form_id, form_link, stage_index, responses_file_path, file_type) VALUES ({0});".format(
                row)
            curser.execute(query)
        self.__conn.commit()

    @staticmethod
    def refresh_formsTablePaths(table: FormsTable, hebrew_table=False):
        header = fr"{os.getcwd()}\data\formsAnswers"
        file_path = "responses_file_path" if not hebrew_table else "מיקום קובץ תשובות"
        file_type = "file_type" if not hebrew_table else "סוג קובץ"
        columns = table.get_cols()
        refreshed = []
        for _, row in table.table.iterrows():
            refreshed_row = []
            for col in columns:
                if col == file_path:
                    path = "{0}\\{1}\\{2}".format(header, row[file_type], row[file_path].split('\\')[-1])
                    refreshed_row.append(path)
                else:
                    refreshed_row.append(row[col])
            refreshed.append(refreshed_row)
        refreshed_table = pd.DataFrame(refreshed, columns=columns)
        table.table = refreshed_table

    def export_formsTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        forms_table = self._get_formsTable()
        if hebrew_table:
            forms_table.columns = [heb for _, _, heb in FormsTable.get_sql_cols()]
        if file_type == 'csv':
            forms_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            forms_table.to_excel(path, index=index)

    def _add_formsAnswers(self, form_answers: FormAnswers):
        curser = self.__conn.cursor()
        query = "INSERT INTO FormsAnswers(email, form_id, row_index, timestamp) VALUES {0};".format(str(form_answers))
        curser.execute(query)
        self.__conn.commit()

    def _get_form_answers_path(self, form_id: str) -> str:
        curser = self.__conn.cursor()
        query = "SELECT responses_file_path FROM Forms WHERE form_id={0}".format(f"\'{form_id}\'")
        curser.execute(query)
        path = pd.DataFrame(curser.fetchall(), columns=["responses_file_path"])['responses_file_path'][0]
        self.__conn.commit()
        return path

    @staticmethod
    def _prepare_form_response(response: list[dict], question_key: str, answer_key: str) -> list:
        row = []
        for d in response:
            question = d[question_key]
            answer = d[answer_key]
            row.append((question, answer))

        return row

    def _already_answered(self, form_id: str, email: str) -> pd.DataFrame:
        curser = self.__conn.cursor()
        query = "SELECT * FROM FormsAnswers WHERE form_id={0} AND email={1};".format(f"\'{form_id}\'", f"\'{email}\'")
        curser.execute(query)
        columns = [col_name for col_name, _, _ in FormsAnswersTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def add_form_response(self, form_id: str, responses_file_type: str, timestamp: str, email: str, response: list[dict]):
        data = Table(path=self._get_form_answers_path(form_id=form_id), table_type=responses_file_type, hebrew_table=True)
        row = SqlServer._prepare_form_response(response=response, question_key='title', answer_key='answer')
        changed = False
        if len(data.get_cols()) == 0:   # set questions if you haven't set them yet
            data.table.columns = [q for q, _ in row]
            changed = True
        already_answered = self._already_answered(form_id=form_id, email=email)  # check if already answered and get the relevant sql row
        if len(already_answered.index) == 0:
            # no answer found
            row_index = len(data.table.index)
            data.table.loc[row_index] = [a for _, a in row]  # add row
            changed = True
            self._add_formsAnswers(form_answers=FormAnswers(email=email, form_id=form_id, row_index=row_index+1, timestamp=timestamp))
            # add answer indicator
        else:
            # there is old answer
            row_index = int(already_answered['row_index']) - 1
            old_timestamp = already_answered['timestamp']
            if Timestamp(timestamp=timestamp) > Timestamp(timestamp=old_timestamp):
                # the old answer is older than the current one
                data.table.loc[row_index] = [a for _, a in row]
                changed = True
        if changed:
            # if any changes were made save the answers data in the file
            data.save_changes()

    def _get_formsAnswersTable(self) -> pd.DataFrame:
        curser = self.__conn.cursor()
        query = "SELECT * FROM FormsAnswers;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in FormsAnswersTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_formsAnswersTable(self, path: str, file_type: str, hebrew_table: bool = False):
        table = FormsAnswersTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=FormsAnswersTable.get_sql_cols()):
            query = "INSERT INTO FormsAnswers(email, form_id, row_index, timestamp) VALUES ({0});".format(row)
            curser.execute(query)
        self.__conn.commit()

    def export_formsAnswersTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        forms_answers_table = self._get_formsAnswersTable()
        if hebrew_table:
            forms_answers_table.columns = [heb for _, _, heb in FormsAnswersTable.get_sql_cols()]
        if file_type == 'csv':
            forms_answers_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            forms_answers_table.to_excel(path, index=index)

    def add_candidate(self, candidate: Candidate):
        curser = self.__conn.cursor()
        query = "INSERT INTO Candidates(email, first_name, last_name, stage_index, status) VALUES {0};".format(
            str(candidate))
        curser.execute(query)
        self.__conn.commit()

    def get_candidatesTable(self) -> pd.DataFrame:
        curser = self.__conn.cursor()
        query = "SELECT * FROM Candidates;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in CandidatesTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def get_candidate_summarized(self, email: str) -> list[dict]:
        curser = self.__conn.cursor()
        query = "SELECT * FROM Candidates WHERE email={0};".format(f"\'{email}\'")
        curser.execute(query)
        columns = [col_name for col_name, _, _ in CandidatesTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()

        if data.shape[0] != 1:
            return []
        else:
            candidate = Candidate(email=email,
                                  first_name=data['first_name'][0],
                                  last_name=data['last_name'][0],
                                  stage_index=data['stage_index'][0],
                                  status=data['status'][0])
            return candidate.to_json_list()

    def get_candidate_forms_info(self, email: str) -> list[tuple[int, list[dict]]]:
        curser = self.__conn.cursor()
        relevant_forms = "SELECT F.stage_index, F.responses_file_path, F.file_type, A.row_index FROM Candidates AS C, Forms AS F, FormsAnswers AS A " \
                         "WHERE C.stage_index >= F.stage_index AND C.email={0} AND F.form_id=A.form_id AND C.email=A.email" \
                         " ORDER BY C.stage_index DESC;".format(f"\'{email}\'")
        curser.execute(relevant_forms)
        relevant_forms = pd.DataFrame(curser.fetchall(), columns=["stage_index", "file_path", "file_type", "row_index"])

        forms = []
        for _, row in relevant_forms.iterrows():
            stage_index = int(row['stage_index'])
            file_path = row['file_path']
            file_type = row['file_type']
            row_index = row['row_index']
            form_answers = Table.get_row_as_json_list(path=file_path, file_type=file_type, row_index=row_index)
            forms.append((stage_index, form_answers))
        self.__conn.commit()
        return forms

    def get_candidate_generalQuestions_info(self, email: str) -> list[tuple[int, list[dict]]]:
        curser = self.__conn.cursor()
        general = []
        general_questions = "SELECT G.stage_index, G.file_path, G.file_type FROM Candidates AS C, GeneralQuestions AS G " \
                            "WHERE C.stage_index >= G.stage_index AND email={0} ORDER BY C.stage_index DESC;".format(f"\'{email}\'")
        curser.execute(general_questions)
        general_questions = pd.DataFrame(curser.fetchall(), columns=["stage_index", "file_path", "file_type"])
        for _, row in general_questions.iterrows():
            stage_index = int(row['stage_index'])
            file_path = row['file_path']
            file_type = row['file_type']
            row = Table.find_row(path=file_path, file_type=file_type, english_key="email", hebrew_key='דוא"ל',
                                 value=email)
            general_answers = Table.questions_row_to_json_list(row=row, english_key="email", hebrew_key='דוא"ל',
                                                               include_key=False)
            general.append((stage_index, general_answers))
        self.__conn.commit()
        return general

    def get_candidate_privateQuestions_info(self, email: str) -> list[tuple[int, list[dict]]]:
        curser = self.__conn.cursor()
        private = []
        private_questions = "SELECT P.stage_index, P.table_path, P.file_type FROM Candidates AS C, PrivateQuestions AS P " \
                            "WHERE C.stage_index >= P.stage_index AND C.email=P.email AND C.email={0} " \
                            "ORDER BY C.stage_index DESC;".format(f"\'{email}\'")
        curser.execute(private_questions)
        private_questions = pd.DataFrame(curser.fetchall(), columns=["stage_index", "file_path", "file_type"])
        for _, row in private_questions.iterrows():
            stage_index = int(row['stage_index'])
            file_path = row['file_path']
            file_type = row['file_type']
            row = Table.get_row(path=file_path, file_type=file_type, row_index=1)
            private_answers = Table.questions_row_to_json_list(row=row)
            private.append((stage_index, private_answers))
        self.__conn.commit()
        return private

    def get_candidate_grades_info(self, email: str):
        curser = self.__conn.cursor()
        grades = []
        grades_query = "SELECT G.stage_index, G.grade, G.passed, G.notes FROM Candidates AS C, Grades AS G " \
                       "WHERE C.email=G.email AND C.email={0} AND C.stage_index >= G.stage_index".format(f"\'{email}\'")

        curser.execute(grades_query)
        grades_table = pd.DataFrame(curser.fetchall(), columns=["stage_index", "grade", "passed", "notes"])
        for _, row in grades_table.iterrows():
            stage_index = int(row['stage_index'])
            g = row['grade']
            passed = row['passed']
            notes = row['notes']
            grade = Grade(email=email, stage_index=stage_index, grade=g, passed=passed, notes=notes)
            grades.append((stage_index, grade.to_json_list()))

        self.__conn.commit()
        return grades

    def get_candidate_entire_info(self, email: str) -> list[dict]:
        general = self.get_candidate_generalQuestions_info(email=email)
        forms = self.get_candidate_forms_info(email=email)
        private = self.get_candidate_privateQuestions_info(email=email)
        grades = self.get_candidate_grades_info(email=email)

        curser = self.__conn.cursor()
        query = "SELECT * FROM Candidates WHERE email={0};".format(f"\'{email}\'")
        curser.execute(query)
        candidate = pd.DataFrame(curser.fetchall(),
                                 columns=["email", "first_name", "last_name", "stage_index", "status"])
        stage_index = candidate['stage_index'][0]
        first_name = candidate['first_name'][0]
        last_name = candidate['last_name'][0]
        status = candidate['status'][0]
        candidate = Candidate(email=email, first_name=first_name, last_name=last_name, stage_index=stage_index,
                              status=status)
        self.__conn.commit()

        stages_table = self.get_stagesTable()
        stages = []
        answers = candidate.to_json_list()[0]
        for index in range(stage_index + 1):
            answer = dict()
            answer['stage_index'] = stages_table['stage_index'][index]
            answer['stage_name'] = stages_table['stage_name'][index]

            # the inner list has at most one list[dict]
            answer['general'] = sum([list_dict for stage_index, list_dict in general if stage_index == index], [])

            # the inner list has at most one list[dict]
            answer['private'] = sum([list_dict for stage_index, list_dict in private if stage_index == index], [])

            # the inner list has one list[dict] for each form tha candidate answered that relevant to the current stage index
            answer['forms'] = sum([list_dict for stage_index, list_dict in forms if stage_index == index], [])

            # the inner list has at most one list[dict]
            answer['grade_info'] = sum([list_dict for stage_index, list_dict in grades if stage_index == index], [])

            stages.append(answer)
        answers['stages'] = stages
        return [answers]

    def load_candidatesTable(self, path: str, file_type: str, hebrew_table: bool = False):
        table = CandidatesTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=CandidatesTable.get_sql_cols()):
            query = "INSERT INTO Candidates(email, first_name, last_name, stage_index, status) VALUES ({0});".format(
                row)
            curser.execute(query)
        self.__conn.commit()

    def export_candidatesTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        candidates_table = self.get_candidatesTable()
        if hebrew_table:
            candidates_table.columns = [heb for _, _, heb in CandidatesTable.get_sql_cols()]
        if file_type == 'csv':
            candidates_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            candidates_table.to_excel(path, index=index)

    def add_generalQuestions(self, general_questions: GeneralQuestions):
        curser = self.__conn.cursor()
        query = "INSERT INTO GeneralQuestions(stage_index, file_path, file_type) VALUES {0};".format(
            str(general_questions))
        curser.execute(query)
        self.__conn.commit()

    def _get_generalQuestionsTable(self) -> pd.DataFrame:
        curser = self.__conn.cursor()
        query = "SELECT * FROM GeneralQuestions;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in GeneralQuestionsTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_generalQuestionsTable(self, path: str, file_type: str, hebrew_table: bool = False):
        table = GeneralQuestionsTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        SqlServer.refresh_generalQuestionsTablePaths(table=table, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=GeneralQuestionsTable.get_sql_cols()):
            query = "INSERT INTO GeneralQuestions(stage_index, file_path, file_type) VALUES ({0});".format(
                row)
            curser.execute(query)
        self.__conn.commit()

    @staticmethod
    def refresh_generalQuestionsTablePaths(table: GeneralQuestionsTable, hebrew_table=False):
        header = fr"{os.getcwd()}\data\generalQuestions"
        file_path = "file_path" if not hebrew_table else "מיקום קובץ"
        file_type = "file_type" if not hebrew_table else "סוג קובץ"
        columns = table.get_cols()
        refreshed = []
        for _, row in table.table.iterrows():
            refreshed_row = []
            for col in columns:
                if col == file_path:
                    path = "{0}\\{1}\\{2}".format(header, row[file_type], row[file_path].split('\\')[-1])
                    refreshed_row.append(path)
                else:
                    refreshed_row.append(row[col])
            refreshed.append(refreshed_row)
        refreshed_table = pd.DataFrame(refreshed, columns=columns)
        table.table = refreshed_table

    def export_generalQuestionsTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        general_questions_table = self._get_generalQuestionsTable()
        if hebrew_table:
            general_questions_table.columns = [heb for _, _, heb in GeneralQuestionsTable.get_sql_cols()]
        if file_type == 'csv':
            general_questions_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            general_questions_table.to_excel(path, index=index)

    def search_candidates(self, condition: str) -> list[dict]:
        variables = CandidatesTable.get_sql_cols()
        sql_cond = SqlServer._parse_condition(condition=condition, variables=variables)
        if not sql_cond:
            return []
        else:
            curser = self.__conn.cursor()
            query = "SELECT * FROM Candidates WHERE {0};".format(sql_cond)
            curser.execute(query)
            data = pd.DataFrame(curser.fetchall(), columns=[eng for eng, _, _ in variables])
            if len(data.index) == 0:
                return []
            else:
                res = []
                for _, row in data.iterrows():
                    candidate = Candidate(email=row['email'],
                                          first_name=row['first_name'],
                                          last_name=row['last_name'],
                                          stage_index=row['stage_index'],
                                          status=row['status'])
                    res.append(candidate.to_json_list())

                return sum(res, [])

    @staticmethod
    def _parse_condition(condition: str, variables: list[tuple[str, str, str]]) -> str | None:
        condition = condition.strip()
        conditions = [cond for cond in condition.split(",") if cond != '']
        sql_conditions = []
        print(conditions)
        for cond in conditions:
            key_val = cond.split("=")
            if len(key_val) != 2:
                return None
            pack = SqlServer._get_key_val_type(key_val=key_val, variables=variables)
            if not pack:
                return None
            else:
                key, val, val_type = pack
                if val_type == 'str':
                    if val:
                        sql_conditions.append(f"{key}=\'{val}\'")
                    else:
                        sql_conditions.append(f"{key} IS NULL")
                elif val_type == 'int':
                    if val:
                        sql_conditions.append(f"{key}={val}")
                    else:
                        sql_conditions.append(f"{key} IS NULL")
        sql_cond = " AND ".join(sql_conditions)
        return sql_cond.strip()

    @staticmethod
    def _get_key_val_type(key_val: list[str], variables: list[tuple[str, str, str]]) -> tuple[str, str, str] | None:
        key_val[0] = key_val[0].strip()
        key_val[1] = key_val[1].strip()
        for eng_symbol, var_type, heb_symbol in variables:
            key, val, t = eng_symbol, None, var_type
            if key_val[0] == heb_symbol:
                val = key_val[1]
            elif key_val[1] == heb_symbol:
                val = key_val[0]

            if val:
                if val == 'ריק':
                    val = None
                return key, val, t
        return None
