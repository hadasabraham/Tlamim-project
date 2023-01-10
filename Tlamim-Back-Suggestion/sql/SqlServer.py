import sqlite3 as sql
import pandas as pd

from entities.stage import Stage
from entities.form import Form
from entities.candidate import Candidate
from entities.grade import Grade


class SqlServer(object):

    def __init__(self, database='test_database'):
        self.__conn = sql.connect(database=database)

    def create_tables(self):
        curser = self.__conn.cursor()

        query = "CREATE TABLE IF NOT EXISTS Stages(stage_index INTEGER PRIMARY KEY, stage_name TEXT NOT NULL, " \
                "CHECK(stage_index >= 0));"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS Forms(stage_index INTEGER NOT NULL, form_id TEXT, form_link TEXT, " \
                " PRIMARY KEY(form_id, form_link, stage_index), FOREIGN KEY (stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS Candidates(email TEXT PRIMARY KEY," \
                " first_name TEXT NOT NULL, last_name TEXT NOT NULL, stage_index INTEGER," \
                " current_status TEXT, FOREIGN KEY (stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS GeneralQuestions(stage_index INTEGER PRIMARY KEY, questions TEXT NOT NULL," \
                " FOREIGN KEY(stage_index) REFERENCES Stages(stage_index));"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS GeneralAnswers(stage_index INTEGER, email TEXT, answers TEXT NOT NULL, PRIMARY KEY(stage_index, email), " \
                "FOREIGN KEY(stage_index) REFERENCES Stages(stage_index), FOREIGN KEY(email) REFERENCES Candidates(email));"

        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS PrivateQuestionsAnswers(stage_index INTEGER, email TEXT, questions TEXT NOT NULL," \
                " answers TEXT NOT NULL, FOREIGN KEY(stage_index) REFERENCES Stages(stage_index), " \
                "FOREIGN KEY(email) REFERENCES Candidates(email), PRIMARY KEY(stage_index, email));"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS CandidatesFormsAnswers(stage_index TEXT, form_id TEXT, " \
                "candidate_email TEXT, response TEXT NOT NULL, PRIMARY KEY(stage_index, candidate_email, form_id)," \
                " FOREIGN KEY(candidate_email) REFERENCES Candidates(email) ON DELETE CASCADE," \
                " FOREIGN KEY(form_id, stage_index) REFERENCES Forms(form_id, stage_index) ON DELETE CASCADE);"
        curser.execute(query)

        query = "CREATE TABLE IF NOT EXISTS Grades(stage_index INTEGER, " \
                "candidate_email TEXT, grade FLOAT, notes TEXT,passed BOOL, " \
                "PRIMARY KEY(stage_index, candidate_email), " \
                "FOREIGN KEY(stage_index) REFERENCES Stages(stage_index) ON DELETE CASCADE, " \
                "FOREIGN KEY(candidate_email) REFERENCES Candidates(candidate_email) ON DELETE CASCADE);"
        curser.execute(query)
        self.__conn.commit()

    def add_stage(self, stage: Stage):

        curser = self.__conn.cursor()
        query = "INSERT INTO Stages(stage_index, stage_name) VALUES ({0}, {1})".format(stage.index,
                                                                                       f"'{stage.name}'")
        curser.execute(query)
        self.__conn.commit()

        if stage.forms:
            for form in stage.forms:
                self.add_form(form=form, stage_index=stage.index)

    def get_stages(self):
        curser = self.__conn.cursor()
        query = "SELECT * FROM Stages ORDER BY stage_index"
        curser.execute(query)

        eng_col = [eng for eng, _, _ in Stage.get_attributes_info()]
        res = pd.DataFrame(curser.fetchall(), columns=eng_col)
        self.__conn.commit()
        return res

    def add_form(self, form: Form, stage_index):
        curser = self.__conn.cursor()

        query = "INSERT INTO Forms(stage_index, form_id, form_link) VALUES " \
                "({0}, {1}, {2})".format(stage_index, f"'{form.id}'", f"'{form.link}'")

        curser.execute(query)
        self.__conn.commit()

    def get_forms(self):
        curser = self.__conn.cursor()
        query = "SELECT * FROM Forms ORDER BY stage_index"
        curser.execute(query)

        eng_col = [eng for eng, _, _ in Form.get_attributes_info()]
        res = pd.DataFrame(curser.fetchall(), columns=eng_col)
        self.__conn.commit()
        return res

    def add_candidate(self, candidate: Candidate):
        curser = self.__conn.cursor()

        query = "INSERT INTO Candidates(email, first_name, last_name, stage_index, current_status) VALUES " \
                "({0}, {1}, {2}, {3}, {4})".format(f"'{candidate.email}'",
                                                   f"'{candidate.first_name}'",
                                                   f"'{candidate.last_name}'",
                                                   candidate.stage_index,
                                                   f"'{candidate.status}'")

        curser.execute(query)
        self.__conn.commit()

    def get_candidates(self):
        curser = self.__conn.cursor()

        query = "SELECT * FROM Candidates ORDER BY email"
        curser.execute(query)

        eng_col = [eng for eng, _, _ in Candidate.get_attributes_info()]
        res = pd.DataFrame(curser.fetchall(), columns=eng_col)

        self.__conn.commit()
        return res

    def add_grade(self, candidate_email: str, grade: Grade):
        curser = self.__conn.cursor()

        if grade.notes is not None and grade.passed is not None:
            query = "INSERT INTO Grades(stage_index, candidate_email, grade, notes, passed) VALUES " \
                    "({0}, {1}, {2}, {3}, {4});".format(grade.stage,
                                                        f"'{candidate_email}'",
                                                        grade.grade,
                                                        f"'{grade.get_notes_str()}'",
                                                        (1 if grade.passed else 0))
            curser.execute(query)
        else:
            print("Error, ", grade.notes is None, grade.passed is None)
        self.__conn.commit()

    def get_grades(self):
        curser = self.__conn.cursor()
        query = "SELECT * FROM Grades ORDER BY candidate_email"

        curser.execute(query)

        eng_col = [eng for eng, _, _ in Grade.get_attributes_info()]
        res = pd.DataFrame(curser.fetchall(), columns=eng_col)
        self.__conn.commit()
        return res

    def drop_tables(self):
        curser = self.__conn.cursor()

        query = "DROP TABLE IF EXISTS Grades;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS CandidatesFormsAnswers;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS PrivateQuestionsAnswers;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS GeneralAnswers;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS GeneralQuestions;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS Candidates;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS Forms;"
        curser.execute(query)

        query = "DROP TABLE IF EXISTS Stages;"
        curser.execute(query)

        self.__conn.commit()

    def clear_table(self):
        curser = self.__conn.cursor()

        query = "DELETE FROM TABLE IF EXISTS Grades;"
        curser.execute(query)

        query = "DELETE FROM TABLE IF EXISTS CandidatesFormsAnswers;"
        curser.execute(query)

        query = "DELETE FROM TABLE IF EXISTS PrivateQuestionsAnswers;"
        curser.execute(query)

        query = "DELETE FROM TABLE IF EXISTS GeneralAnswers;"
        curser.execute(query)

        query = "DELETE FROM TABLE IF EXISTS GeneralQuestions;"
        curser.execute(query)

        query = "DELETE FROM TABLE IF EXISTS Candidates;"
        curser.execute(query)

        query = "DELETE FROM TABLE IF EXISTS Forms;"
        curser.execute(query)

        query = "DELETE FROM TABLE IF EXISTS Stages;"
        curser.execute(query)

        self.__conn.commit()

    def get_candidates_general_information(self, condition: str):
        """

        :param condition: condition only on the general information attributes
        :return:
        """
        curser = self.__conn.cursor()

        query = "SELECT * FROM Candidates {0};".format(
            SqlServer.parse_condition(condition=condition, columns=Candidate.get_attributes_info()))
        curser.execute(query)

        eng_col = [eng for eng, _, _ in Candidate.get_attributes_info()]
        df = pd.DataFrame(curser.fetchall(),
                          columns=eng_col)
        self.__conn.commit()

        return SqlServer.dataframe_to_json_list(df=df, columns=eng_col)

    @staticmethod
    def parse_condition(condition: str, columns: list[tuple[str, str, str]]):
        """

        :param condition:
        :param columns: list of tuples of (eng_col, heb_col, type string)
        :return:
        """
        error_cond = "WHERE FALSE"
        res = "WHERE"
        attributes = condition.split(",")
        for attr in attributes:
            clean = attr.strip()
            cond = clean.split(" ")
            item1 = (cond[0]).strip()
            item2 = (cond[1]).strip()

            key_eng = ''
            type_str = ''
            val = ''
            for eng_cmp, key_cmp, type_str_cmp in columns:
                if key_cmp == item1:
                    key_eng = eng_cmp
                    type_str = type_str_cmp
                    val = item2
                    break
                elif key_cmp == item2:
                    key_eng = eng_cmp
                    type_str = type_str_cmp
                    val = item1

            if not key_eng or not type_str:
                # if not found this is not valid key
                return error_cond

            if type_str == 'str':
                res += f" {key_eng}='{val}' AND"
            else:
                res += f" {key_eng}={val} AND"

        # the rfind returns a valid value because if there was error and the AND not in the res then we returned already
        return res[:res.rfind(" AND")]

    @staticmethod
    def dataframe_to_json_list(df: pd.DataFrame, columns: list[str]):
        res = []

        for index, row in df.iterrows():
            d = {}
            for col_name in columns:
                d[col_name] = row[col_name]
            res.append(d)

        return res

    def get_candidate_entire_information(self, candidate_email: str):
        """
        Gather the entire information collected on specific candidate from all of his stages
        :param candidate_email:
        :return:
        """
        pass

    def get_candidate_stage_information(self, candidate_email: str, stage_index: int):
        """
        Get the information of a candidate that relevant to a specific stage
        :param candidate_email:
        :param stage_index:
        :return:
        """
        pass

    def search(self):
        pass

    def close_stage(self, stage_index):
        """
        Decide to eliminate all the candidates that haven't passed the stage with stage_index until now.
        In the decisions notes add the note: "timeout" for the relevant candidates
        :param stage_index:
        :return:
        """
        pass

    def load_csv(self, stages_path, general_information_path, answers_path, grades_path, decisions_path):
        """
        load all the tables from csv
        :return:
        """
        pass

    def export_csv(self, stages_path, general_information_path, answers_path, grades_path, decisions_path):
        """
        export all the tables to csv
        :return:
        """
        pass

    """
    General tables description:
    
    Stages(stage_index INTEGER PRIMARY KEY, stage_name TEXT)
    
    
    Forms(form_id TEXT, form_link TEXT, stage_index INTEGER, PRIMARY KEY(form_id, form_link))
    # Stage without form will insert form_id=''
    
    
    Candidates(email TEXT PRIMARY KEY, first_name TEXT NOT NULL, family_name TEXT NOT NULL,
     stage_index INTEGER, current_status TEXT, FOREIGN KEY (stage_id) REFERENCES Stages(stage_index) ON DELETE CASCADE)
     
    
    CandidatesAnswers(stage_index TEXT, form_id TEXT, candidate_email TEXT, response TEXT, PRIMARY KEY(stage_index, candidate_email))
    # The response structure is a string of dictionary with the key-values:
    # * 'stage_name' : '<name>'
    # * 'timestamp' : '<timestamp>'
    # * 'answers' : '<answers>'
    # Where the answers value is a list of dictionaries of the format:
    # * 'question_title' : '<title>'
    # * 'question_answer' : '<answer>'
    
    We can add column to timestamp if we wish to update a response without need to parse the existing one 
    (the response string is big so might be better to get the timestamp separately and if need updating the response content). 
    
    Notice that if form_id is 0 and we wish to load data from a table that has questions as its columns and the rows are different candidate
    We can parse each row by identifying the candidate email and which stage the table represent.
    We assume the table has timestamp for each row so the general answers structure can be built.
    The answers list of dictionaries can be built by parsing each colum in the row.
    We use the column title as the question title and the value of the specific column within the row as
    the question answer.
    This is important if we wish to be able to parse Eleazar current export tables.
    For now we assume that stage 0 is the input information. It doesn't have a form and if in the csv there is no column 
    to indicate the stage we assume that this is stage 0.
    
    
    Grades(stage_index INTEGER, candidate_email TEXT, grade FLOAT, notes TEXT,pass BOOL, PRIMARY KEY(stage_index, candidate_email))
    # saving the relevant grades foreach candidate stage
    
        
    Notice that we can merge the grades and decisions tables if we add different notes column for each step or if we save the notes
    as a string of list.
    Suggested format could be list of dictionaries with the format:
    * 'note_index': '<index>'
    * 'note': '<note>'
    * 'step': '<step>'
    When the step could be grading, deciding as basic and might be extended in the future
    
    
    * General search - Roy
    * Get General Info - Roy
    * Get questions info - Roy
    * Create/Clear/Delete - Roy 
    * Add Stage/Form - Roy
    
    * Load info - Alon
    * Export info - Alon
    
    * Sanity check
    
    """
