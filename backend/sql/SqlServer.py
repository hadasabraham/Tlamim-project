import os
import shutil
import sqlite3 as sql
from datetime import datetime
import json

from distutils.dir_util import copy_tree
from sql.entities.stage import Stage
from sql.entities.form import Form
from sql.entities.candidate import Candidate
from sql.entities.grade import Grade
from sql.entities.generalQuestions import GeneralQuestions
from sql.entities.formAnswers import FormAnswers
from sql.entities.privateQuestions import PrivateQuestions
from sql.entities.timestamp import Timestamp
from sql.entities.table import *


class SqlServer(object):

    def __init__(self, database='test_database'):
        self.__conn = sql.connect(database=database)
        self.registration_info = dict()

    def create_tables(self):
        """
        Crate all the tables if not exists.
        Stages(stage_index, stage_name).
        Stores the general properties of each stage.

        Candidate(email, first_name, last_name, stage_index, status).
        Stores the summarizes information presented on the main page for each candidate.

        GeneralQuestions(stage_index, file_path, file_type).
        Stores a xlsx/csv file full path of a table with general questions as columns and answers as rows.
        The questions are associated with a certain stage by stage_index and each stage can have at most one file (one entry in the sql table).

        Forms(form_id, form_link, stage_index, responses_file_path, file_type).
        Stores the general information about a form questionnaire associated with some stage.
        The responses_file_path and file_type represent the location for saving the answers for the form.
        The path is assumed to be a full path.
        There can be as many forms as the user like to each stage.

        FormsAnswers(email, form_id, row_index, timestamp).
        Stores who answered on each form, when the last answer we parsed was created and in which row in the answers file associated
        with the form, we will find the full answers for the form.


        PrivateQuestions(email, stage_index, table_path, file_type).
        Stores a file with questions as column and one row as answers.
        This files allow to add specific questions and answers given to one candidate at a specific stage.
        Can have at most one entry for each candidate at some stage.

        Grades(email, stage_index, grade, passed, notes).
        Allow the user to grade candidates stage performance and add text notes to the entire stage.
        Here we save whether the candidate passed a specific stage.

        :return:
        """
        curser = self.__conn.cursor()

        query = "CREATE TABLE IF NOT EXISTS Stages(stage_index INTEGER PRIMARY KEY, stage_name TEXT NOT NULL, CHECK(stage_index >= 0));"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS Candidates(email TEXT PRIMARY KEY, first_name TEXT NOT NULL, " \
                "last_name NOT NULL, stage_index INTEGER, status TEXT, timestamp TEXT," \
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
                "grade FLOAT NOT NULL, passed BOOL, notes TEXT, timestamp TEXT, PRIMARY KEY(email, stage_index), " \
                "FOREIGN KEY(email) REFERENCES Candidates(email) ON DELETE CASCADE, " \
                "FOREIGN KEY(stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        self.__conn.commit()
        SqlServer.prepare_inner_directories()
        base_path = f"{os.getcwd()}{os.path.sep}sql{os.path.sep}data"

        if os.path.exists(f"{base_path}{os.path.sep}registration_form_info.json"):
            with open(f"{base_path}{os.path.sep}registration_form_info.json") as json_file:
                data = json.load(json_file)
                self.registration_info['form_id'] = data['form_id']
                self.registration_info['form_link'] = data['form_link']



    def set_registration_form(self, form_id: str, form_link: str):
        base_path = f"{os.getcwd()}{os.path.sep}sql{os.path.sep}data"
        d = dict()
        d['form_id'] = form_id
        d['form_link'] = form_link
        # Serializing json
        json_object = json.dumps(d, indent=4)

        with open(f"{base_path}{os.path.sep}registration_form_info.json", "w+") as outfile:
            outfile.write(json_object)

        self.registration_info['form_id'] = form_id
        self.registration_info['form_link'] = form_link




    @staticmethod
    def prepare_inner_directories():

        base_path = f"{os.getcwd()}{os.path.sep}sql{os.path.sep}data"
        directories = [fr'{os.path.sep}formsAnswers',
                       fr'{os.path.sep}generalQuestions', fr'{os.path.sep}privateQuestions']
        file_types = ['xlsx', 'csv']

        if not os.path.exists(base_path):
            os.makedirs(base_path, mode=0o777)

        for directory in directories:
            for f_type in file_types:
                path = f'{base_path}{directory}{os.path.sep}{f_type}'
                if not os.path.exists(path):
                    os.makedirs(path, mode=0o777)

        if not os.path.exists(fr'{base_path}{os.path.sep}snapshots'):
            os.makedirs(fr'{base_path}{os.path.sep}snapshots', mode=0o777)

    @staticmethod
    def clear_inner_directories():
        base_path = f"{os.getcwd()}{os.path.sep}sql{os.path.sep}data"
        directories = [fr'{os.path.sep}formsAnswers',
                       fr'{os.path.sep}generalQuestions', fr'{os.path.sep}privateQuestions']
        file_types = ['xlsx', 'csv']

        for directory in directories:
            for f_type in file_types:
                path = f'{base_path}{directory}{os.path.sep}{f_type}'
                if os.path.exists(path):
                    shutil.rmtree(path)

        if os.path.exists(f"{base_path}{os.path.sep}registration_form_info.json"):
            os.remove(f"{base_path}{os.path.sep}registration_form_info.json")

    def drop_tables(self):
        """
        Drop all tables from the database if exists.
        Do not delete the form responses files, general questions files or private questions files.
        :return:
        """
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

        SqlServer.clear_inner_directories()

    def clear_tables(self):
        """
        Clear all the tables without clearing/deleting form responses files, general questions files or private questions files.
        :return:
        """
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
        SqlServer.clear_inner_directories()

    def add_stage(self, stage: Stage):
        """
        Adding stage to the stages table
        :param stage: stage object
        :return:
        """
        curser = self.__conn.cursor()
        query = "INSERT INTO Stages(stage_index, stage_name) VALUES {0};".format(str(stage))
        curser.execute(query)
        self.__conn.commit()

    def get_stagesTable(self) -> pd.DataFrame:
        """
        :return: the stages table with the columns 'stage_index', 'stage_name' sorted by 'stage_index' in ascending order.
        """
        curser = self.__conn.cursor()
        query = "SELECT * FROM Stages ORDER BY stage_index ASC;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in StagesTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_stagesTable(self, path: str, file_type: str, hebrew_table: bool):
        """
        Loads stages table represent the general information on the stages in the selection process.
        The stages table structure detailed in the StagesTable object in table.py
        :param path: a path of table file
        :param file_type: the stages file type
        :param hebrew_table: is the columns in hebrew or english
        :return:
        """
        table = StagesTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=StagesTable.get_sql_cols()):
            query = "INSERT INTO Stages(stage_index, stage_name) VALUES ({0});".format(row)
            curser.execute(query)
        self.__conn.commit()

    def export_stagesTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        """
        Saves the information from get_stagesTable to a file
        :param path: where to save the table
        :param file_type: xlsx/csv
        :param index: save indexes  (generally use no)
        :param hebrew_table: columns names should be in hebrew
        :return:
        """
        stages_table = self.get_stagesTable()
        if hebrew_table:
            stages_table.columns = [heb for _, _, heb in StagesTable.get_sql_cols()]

        if file_type == 'csv':
            stages_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            stages_table.to_excel(path, index=index)

    def _add_grade(self, grade: Grade):
        """
        Adding grade to the database
        :param grade: grade object
        :return:
        """
        curser = self.__conn.cursor()
        query = "INSERT INTO Grades(email, stage_index, grade, passed, notes, timestamp) VALUES {0};".format(str(grade))
        curser.execute(query)
        self.__conn.commit()

    def update_grade(self, grade: Grade):
        curser = self.__conn.cursor()
        query = "SELECT stage_index FROM Candidates WHERE email={0}".format(f"\'{grade.email}\'")
        curser.execute(query)
        valid_stage_index = pd.DataFrame(curser.fetchall(), columns=["stage_index"])
        if len(valid_stage_index.index) == 0:
            return  # candidate not found
        valid_stage_index = valid_stage_index["stage_index"][
                                0] >= grade.stage_index  # can update only stages the candidate passed
        if valid_stage_index:
            query = "SELECT * FROM Grades WHERE stage_index={0} AND email={1}".format(f"{grade.stage_index}",
                                                                                      f"\'{grade.email}\'")
            curser.execute(query)
            exists = pd.DataFrame(curser.fetchall(), columns=[eng for eng, _, _ in GradesTable.get_sql_cols()])
            if len(exists.index) == 0:
                # no grade ever inserted. assume that the grade has all its necessary entries
                if grade.grade is None:
                    return
                self._add_grade(grade=grade)
            else:
                # updating old grade. Assume that each one of the grade, passed, notes can be updated.
                # if the parameter is None assume no update required
                # the notes are accumulative
                # passed stages can be None, True, False. valid updates are None -> False -> True, or, None -> True -> False
                # automatic email will be sent upon request to all the candidates who passed the stage
                current_grade = Grade(email=exists["email"][0],
                                      stage_index=exists["stage_index"][0],
                                      grade=exists["grade"][0],
                                      passed=exists["passed"][0],
                                      notes=exists["notes"][0],
                                      timestamp=exists["timestamp"][0])

                current_grade.update_timestamp(grade.timestamp)
                passed_changed = current_grade.update_passed(passed=grade.passed)
                score_changed = current_grade.update_score(score=grade.grade)
                notes_changed = current_grade.update_notes(notes=grade.notes)
                if passed_changed:
                    query = "UPDATE Grades SET passed={0}, timestamp={1} WHERE stage_index={2} AND email={3}".format(
                        f"{current_grade.passed}",
                        f"\'{current_grade.timestamp}\'",
                        f"{current_grade.stage_index}",
                        f"\'{current_grade.email}\'")
                    curser.execute(query)
                    if current_grade.passed:  # automatic advancement of candidate
                        self.advance_candidate(email=current_grade.email)
                    else:
                        self.update_candidate_timestamp(email=current_grade.email, timestamp=current_grade.timestamp)

                if score_changed:
                    query = "UPDATE Grades SET grade={0} WHERE stage_index={1} AND email={2}".format(
                        f"{current_grade.grade}",
                        f"{current_grade.stage_index}",
                        f"\'{current_grade.email}\'")
                    curser.execute(query)
                if notes_changed:
                    query = "UPDATE Grades SET notes={0} WHERE stage_index={1} AND email={2}".format(
                        f"\'{current_grade.notes}\'",
                        f"{current_grade.stage_index}",
                        f"\'{current_grade.email}\'")
                    curser.execute(query)
                self.__conn.commit()

    def get_gradesTable(self) -> pd.DataFrame:
        """
        :return: grades table with columns 'email', 'stage_index', 'grade', 'passed' and 'notes'.
        """
        curser = self.__conn.cursor()
        query = "SELECT * FROM Grades;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in GradesTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_gradesTable(self, path: str, file_type: str, hebrew_table: bool = False):
        """
        Loads grades table for the selection process.
        The grades table structure detailed in the GradesTable object in table.py
        :param path: a path of table file
        :param file_type: the stages file type
        :param hebrew_table: is the columns in hebrew or english
        """
        table = GradesTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=GradesTable.get_sql_cols()):
            query = "INSERT INTO Grades(email, stage_index, grade, passed, notes, timestamp) VALUES ({0});".format(row)
            curser.execute(query)
        self.__conn.commit()

    def export_gradesTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        """
        Saves the information from get_gradesTable to a file
        :param path: where to save the table
        :param file_type: xlsx/csv
        :param index: save indexes  (generally use no)
        :param hebrew_table: columns names should be in hebrew
        """
        grades_table = self.get_gradesTable()
        if hebrew_table:
            grades_table.columns = [heb for _, _, heb in GradesTable.get_sql_cols()]
        if file_type == 'csv':
            grades_table.to_csv(path, index=index)
        elif file_type == 'xlsx':
            grades_table.to_excel(path, index=index)

    def add_privateQuestions(self, private_questions: PrivateQuestions):
        """
        Adds private questions file
        :param private_questions: private questions object (creates copy of the file to our data/privateQuestions directory)
        :return:
        """
        curser = self.__conn.cursor()
        query = "INSERT INTO PrivateQuestions(email, stage_index, table_path, file_type) VALUES {0};".format(
            str(private_questions))
        curser.execute(query)
        self.__conn.commit()

    def _get_privateQuestionsTable(self) -> pd.DataFrame:
        """
        :return:  private questions table with columns 'email', 'stage_index', 'table_path' and 'file_type'
        """
        curser = self.__conn.cursor()
        query = "SELECT * FROM PrivateQuestions;"
        curser.execute(query)
        columns = [col_name for col_name, _, _ in PrivateQuestionsTable.get_sql_cols()]
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

    def load_privateQuestionsTable(self, path: str, file_type: str, hebrew_table: bool = False):
        """
        Loads private questions table for the selection process.
        The private questions  table structure detailed in the PrivateQuestionsTable object in table.py .
        Refresh the 'table_path' because the full path can change but the relative path in the data directory cannot
        :param path: a path of table file
        :param file_type: the stages file type
        :param hebrew_table: is the columns in hebrew or english
        :return:
        """
        table = PrivateQuestionsTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        SqlServer.refresh_privateQuestionsTablePaths(table=table, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=PrivateQuestionsTable.get_sql_cols()):
            query = "INSERT INTO PrivateQuestions(email, stage_index, table_path, file_type) VALUES ({0});".format(row)
            curser.execute(query)
        self.__conn.commit()

    @staticmethod
    def refresh_privateQuestionsTablePaths(table: PrivateQuestionsTable, hebrew_table=False):
        """
        Refresh all 'table_path' for all the private questions table
        :param table: a PrivateQuestionsTable object
        :param hebrew_table: is the columns in hebrew or english
        :return:
        """
        header = fr"{os.getcwd()}{os.path.sep}sql{os.path.sep}data{os.path.sep}privateQuestions"
        file_path = "table_path" if not hebrew_table else "מיקום קובץ"
        file_type = "file_type" if not hebrew_table else "סוג קובץ"
        columns = table.get_cols()
        refreshed = []
        for _, row in table.table.iterrows():
            refreshed_row = []
            for col in columns:
                if col == file_path:
                    file_name = row[file_path].split(f'{os.path.sep}')[-1]
                    path = fr"{header}{os.path.sep}{row[file_type]}{os.path.sep}{file_name}"
                    refreshed_row.append(path)
                else:
                    refreshed_row.append(row[col])
            refreshed.append(refreshed_row)
        refreshed_table = pd.DataFrame(refreshed, columns=columns)
        table.table = refreshed_table

    def export_privateQuestionsTable(self, path: str, file_type: str, index: bool, hebrew_table: bool = False):
        """
        Saves the information from _get_privateQuestionsTable to a file
        :param path: where to save the table
        :param file_type: xlsx/csv
        :param index: save indexes  (generally use no)
        :param hebrew_table: columns names should be in hebrew
        :return:
        """
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

    def get_forms_required_info_to_adding_answer(self):
        curser = self.__conn.cursor()
        query = "SELECT form_id, file_type FROM Forms;"
        curser.execute(query)
        columns = ['form_id', 'file_type']
        data = pd.DataFrame(curser.fetchall(), columns=columns)
        self.__conn.commit()
        return data

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
        header = fr"{os.getcwd()}{os.path.sep}sql{os.path.sep}data{os.path.sep}formsAnswers"
        file_path = "responses_file_path" if not hebrew_table else "מיקום קובץ תשובות"
        file_type = "file_type" if not hebrew_table else "סוג קובץ"
        columns = table.get_cols()
        refreshed = []
        for _, row in table.table.iterrows():
            refreshed_row = []
            for col in columns:
                if col == file_path:
                    file_name = row[file_path].split(f'{os.path.sep}')[-1]
                    path = fr"{header}{os.path.sep}{row[file_type]}{os.path.sep}{file_name}"
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

    def add_form_response(self, form_id: str, responses_file_type: str, timestamp: str, email: str,
                          response: list[dict]):
        data = Table(path=self._get_form_answers_path(form_id=form_id), table_type=responses_file_type,
                     hebrew_table=True)
        row = SqlServer._prepare_form_response(response=response, question_key='title', answer_key='answer')
        changed = False
        if len(data.get_cols()) == 0:  # set questions if you haven't set them yet
            data.delete_and_rename_columns(columns=[q for q, _ in row])
            changed = True
        already_answered = self._already_answered(form_id=form_id,
                                                  email=email)  # check if already answered and get the relevant sql row
        if len(already_answered.index) == 0:
            # no answer found
            row_index = len(data.table.index)
            data.table.loc[row_index] = [a for _, a in row]  # add row
            changed = True
            # add answer indicator
            self._add_formsAnswers(
                form_answers=FormAnswers(email=email, form_id=form_id, row_index=row_index + 1, timestamp=timestamp))
        else:
            # there is old answer
            row_index = int(already_answered['row_index'][0]) - 1
            old_timestamp = str(already_answered['timestamp'][0])
            old_timestamp = str(old_timestamp)
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
        query = "INSERT INTO Candidates(email, first_name, last_name, stage_index, status, timestamp) VALUES {0};".format(
            str(candidate))
        curser.execute(query)
        self.__conn.commit()

    def update_candidate_status(self, email: str, status: str):
        curser = self.__conn.cursor()
        query = "UPDATE Candidates SET status={0} WHERE email={1}".format(f"\'{status}\'", f"\'{email}\'")
        curser.execute(query)
        self.__conn.commit()

    def update_candidate_timestamp(self, email: str, timestamp: str):
        curser = self.__conn.cursor()
        query = "UPDATE Candidates SET timestamp={0} WHERE email={1}".format(f"\'{timestamp}\'", f"\'{email}\'")
        curser.execute(query)
        self.__conn.commit()

    def advance_candidate(self, email: str):
        # when closing a stage all the candidate who passed the stage will advance to the next stage.
        # assume that closing the final stage isn't possible and all those in the final stage with grade.passed = True accepted to the program
        curser = self.__conn.cursor()
        query = "SELECT stage_index FROM Candidates WHERE email={0}".format(f"\'{email}\'")
        curser.execute(query)
        stage_index = pd.DataFrame(curser.fetchall(), columns=["stage_index"])
        if len(stage_index.index) == 0:
            return  # candidate not found
        stage_index = stage_index["stage_index"][0] + 1
        query = "SELECT stage_index FROM Stages WHERE stage_index={0}".format(f"{stage_index}")
        curser.execute(query)
        exists = pd.DataFrame(curser.fetchall(), columns=["stage_index"])
        if len(exists.index) == 0:
            return  # candidate in the last stage can't progress

        timestamp = f"\'{datetime.now()}\'"
        query = "UPDATE Candidates SET stage_index={0}, timestamp={1} WHERE email={2}".format(f"{stage_index}", timestamp, f"\'{email}\'")
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
                                  status=data['status'][0],
                                  timestamp=data['timestamp'][0])
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
                            "WHERE C.stage_index >= G.stage_index AND email={0} ORDER BY C.stage_index DESC;".format(
            f"\'{email}\'")
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

    def get_candidate_grades_info(self, email: str) -> tuple[list, str]:
        curser = self.__conn.cursor()
        grades = []
        grades_query = "SELECT G.stage_index, G.grade, G.passed, G.notes, G.timestamp FROM Candidates AS C, Grades AS G " \
                       "WHERE C.email=G.email AND C.email={0} AND C.stage_index >= G.stage_index ORDER BY G.stage_index DESC;".format(
            f"\'{email}\'")

        curser.execute(grades_query)
        grades_table = pd.DataFrame(curser.fetchall(), columns=["stage_index", "grade", "passed", "notes", "timestamp"])
        all_notes = ""
        for _, row in grades_table.iterrows():
            stage_index = int(row['stage_index'])
            g = row['grade']
            passed = row['passed']
            notes = row['notes']
            if notes is not None:
                all_notes += f"{notes}\r\n"
            timestamp = row['timestamp']
            grade = Grade(email=email, stage_index=stage_index, grade=g, passed=passed, notes=notes, timestamp=timestamp)
            grades.append((stage_index, grade.to_json_list()))

        self.__conn.commit()
        return grades, all_notes

    def get_candidate_entire_info(self, email: str) -> list[dict]:
        general = self.get_candidate_generalQuestions_info(email=email)
        forms = self.get_candidate_forms_info(email=email)
        private = self.get_candidate_privateQuestions_info(email=email)
        grades, all_notes = self.get_candidate_grades_info(email=email)

        curser = self.__conn.cursor()
        query = "SELECT * FROM Candidates WHERE email={0};".format(f"\'{email}\'")
        curser.execute(query)
        candidate = pd.DataFrame(curser.fetchall(),
                                 columns=[eng for eng, _, _ in CandidatesTable.get_sql_cols()])
        if len(candidate.index) == 0:
            return []
        stage_index = candidate['stage_index'][0]
        first_name = candidate['first_name'][0]
        last_name = candidate['last_name'][0]
        status = candidate['status'][0]
        timestamp = candidate['timestamp'][0]
        candidate = Candidate(email=email, first_name=first_name, last_name=last_name, stage_index=stage_index,
                              status=status, timestamp=timestamp)
        self.__conn.commit()

        stages_table = self.get_stagesTable()
        stages = []
        answers = candidate.to_json_list()[0]
        for index in range(stage_index, -1, -1):
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
        answers['all_notes'] = all_notes
        return [answers]

    def load_candidatesTable(self, path: str, file_type: str, hebrew_table: bool = False):
        table = CandidatesTable(path=path, table_type=file_type, hebrew_table=hebrew_table)
        curser = self.__conn.cursor()
        for row in table.get_rows_to_load(sql_columns=CandidatesTable.get_sql_cols()):
            query = "INSERT INTO Candidates(email, first_name, last_name, stage_index, status, timestamp) VALUES ({0});".format(
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
        header = fr"{os.getcwd()}{os.path.sep}sql{os.path.sep}data{os.path.sep}generalQuestions"
        file_path = "file_path" if not hebrew_table else "מיקום קובץ"
        file_type = "file_type" if not hebrew_table else "סוג קובץ"
        columns = table.get_cols()
        refreshed = []
        for _, row in table.table.iterrows():
            refreshed_row = []
            for col in columns:
                if col == file_path:
                    file_name = row[file_path].split(f'{os.path.sep}')[-1]
                    path = fr"{header}{os.path.sep}{row[file_type]}{os.path.sep}{file_name}"
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
                                          status=row['status'],
                                          timestamp=row['timestamp'])
                    res.append(candidate.to_json_list()[0])
                res = sorted(res, key=lambda d: Timestamp(timestamp=d['timestamp']))
                return res

    @staticmethod
    def _parse_condition(condition: str, variables: list[tuple[str, str, str]]) -> str | None:
        condition = condition.strip()
        if condition == "הכול":
            return "TRUE"
        conditions = [cond for cond in condition.split(",") if cond != '']
        sql_conditions = []
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
                        sql_conditions.append(f"{key} LIKE \'%{val}%\'")
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
                if val == "\'ריק\'":
                    val = None
                return key, val, t
        return None

    def save_snapshot(self, snapshot_name):
        base_path = fr"{os.getcwd()}{os.path.sep}sql{os.path.sep}data{os.path.sep}snapshots{os.path.sep}{snapshot_name}"
        if not os.path.exists(base_path):
            os.makedirs(base_path, mode=0o777)

        stages_path = fr"{base_path}{os.path.sep}stagesTable.xlsx"
        self.export_stagesTable(path=stages_path, file_type="xlsx", index=False, hebrew_table=True)

        candidates_path = fr"{base_path}{os.path.sep}candidatesTable.xlsx"
        self.export_candidatesTable(path=candidates_path, file_type="xlsx", index=False, hebrew_table=True)

        forms_path = fr"{base_path}{os.path.sep}formsTable.xlsx"
        self.export_formsTable(path=forms_path, file_type="xlsx", index=False, hebrew_table=True)

        forms_answers_path = fr"{base_path}{os.path.sep}formsAnswersTable.xlsx"
        self.export_formsAnswersTable(path=forms_answers_path, file_type="xlsx", index=False, hebrew_table=True)

        general_questions_path = fr"{base_path}{os.path.sep}generalQuestionsTable.xlsx"
        self.export_generalQuestionsTable(path=general_questions_path, file_type="xlsx", index=False, hebrew_table=True)

        private_questions_path = fr"{base_path}{os.path.sep}privateQuestionsTable.xlsx"
        self.export_privateQuestionsTable(path=private_questions_path, file_type="xlsx", index=False, hebrew_table=True)

        grades_path = fr"{base_path}{os.path.sep}gradesTable.xlsx"
        self.export_gradesTable(path=grades_path, file_type="xlsx", index=False, hebrew_table=True)

        folders = ["formsAnswers", "generalQuestions", "privateQuestions"]
        origin_base = fr"{os.getcwd()}{os.path.sep}sql{os.path.sep}data{os.path.sep}"
        for folder in folders:
            origin_folder = fr"{origin_base}{folder}"
            dest = fr"{base_path}{os.path.sep}{folder}"
            copy_tree(origin_folder, dest)

        origin = f"{origin_base}{os.path.sep}registration_form_info.json"
        dest = fr"{base_path}{os.path.sep}registration_form_info.json"
        shutil.copyfile(origin, dest)

    def load_snapshot(self, snapshot_name):
        base_path = fr"{os.getcwd()}{os.path.sep}sql{os.path.sep}data{os.path.sep}snapshots{os.path.sep}{snapshot_name}"
        if not os.path.exists(base_path):
            return

        stages_path = fr"{base_path}{os.path.sep}stagesTable.xlsx"
        self.load_stagesTable(path=stages_path, file_type="xlsx", hebrew_table=True)

        candidates_path = fr"{base_path}{os.path.sep}candidatesTable.xlsx"
        self.load_candidatesTable(path=candidates_path, file_type="xlsx", hebrew_table=True)

        forms_path = fr"{base_path}{os.path.sep}formsTable.xlsx"
        self.load_formsTable(path=forms_path, file_type="xlsx", hebrew_table=True)

        forms_answers_path = fr"{base_path}{os.path.sep}formsAnswersTable.xlsx"
        self.load_formsAnswersTable(path=forms_answers_path, file_type="xlsx", hebrew_table=True)

        general_questions_path = fr"{base_path}{os.path.sep}generalQuestionsTable.xlsx"
        self.load_generalQuestionsTable(path=general_questions_path, file_type="xlsx", hebrew_table=True)

        private_questions_path = fr"{base_path}{os.path.sep}privateQuestionsTable.xlsx"
        self.load_privateQuestionsTable(path=private_questions_path, file_type="xlsx", hebrew_table=True)

        grades_path = fr"{base_path}{os.path.sep}gradesTable.xlsx"
        self.load_gradesTable(path=grades_path, file_type="xlsx", hebrew_table=True)

        folders = ["formsAnswers", "generalQuestions", "privateQuestions"]
        origin_base = fr"{os.getcwd()}{os.path.sep}sql{os.path.sep}data{os.path.sep}"
        for folder in folders:
            origin_folder = fr"{origin_base}{folder}"
            copy = fr"{base_path}{os.path.sep}{folder}"
            copy_tree(copy, origin_folder)

        origin = f"{origin_base}{os.path.sep}registration_form_info.json"
        copy = fr"{base_path}{os.path.sep}registration_form_info.json"
        if os.path.exists(copy):
            shutil.copyfile(copy, origin)

        if os.path.exists(origin):
            with open(origin) as json_file:
                data = json.load(json_file)
                self.registration_info['form_id'] = data['form_id']
                self.registration_info['form_link'] = data['form_link']
