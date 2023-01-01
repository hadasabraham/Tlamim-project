import sqlite3 as sql
import pandas as pd

from database.candidate import Candidate
from database.grade import Grade
from database.stage import Stage

TRANSLATE_TO_ENGLISH = {"אימייל": "email", "שלב": "stage", "שם": "name"}
TRANSLATE_TO_HEBREW = {"email": "אימייל", "stage": "שלב", "name": "שם"}
CANDIDATE_ENGLISH_COLS_TYPES = {"email": "str", "stage": "int", "name": "str"}


class SqlServer(object):

    def __init__(self, database='test_database'):
        self.conn = sql.connect(database=database)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()

        query = "CREATE TABLE IF NOT EXISTS Stages(stage_id INTEGER PRIMARY KEY, form_link TEXT NOT NULL, CHECK(stage_id >= 1));"
        c.execute(query)

        query = "CREATE TABLE IF NOT EXISTS" \
                " Candidates(email TEXT PRIMARY KEY, name TEXT NOT NULL, stage INTEGER NOT NULL, status TEXT," \
                " CHECK(stage >= 1), FOREIGN KEY (stage) REFERENCES Stages(stage_id) ON DELETE CASCADE);"
        c.execute(query)

        query = "CREATE TABLE IF NOT EXISTS Grades(stage_id INTEGER NOT NULL," \
                " candidate_email TEXT NOT NULL, score INTEGER NOT NULL, " \
                "PRIMARY KEY(stage_id, candidate_email), " \
                "FOREIGN KEY (stage_id) REFERENCES Stages(stage_id) ON DELETE CASCADE, " \
                "FOREIGN KEY (candidate_email) REFERENCES Candidates(email) ON DELETE CASCADE, " \
                "CHECK(score >= 0 AND score <= 10));"
        c.execute(query)

        self.conn.commit()

    def add_stage(self, stage: Stage):
        c = self.conn.cursor()
        query = "INSERT INTO Stages(stage_id, form_link) VALUES ({0}, '{1}');" \
            .format(stage.stage_id, stage.form_link)

        c.execute(query)
        self.conn.commit()

    def load_stages_table_from_csv(self, path):
        """
        param path: a path to csv table with columns stage_id, form_link
        :return:
        """
        try:
            c = self.conn.cursor()
            df = pd.read_csv(fr'{path}')
            values = SqlServer._dataframe_to_database_values(df)

            query = "INSERT INTO Stages(stage_id, form_link) VALUES {0};".format(values)
            c.execute(query)
        except Exception as e:
            print(e)
        finally:
            self.conn.commit()

    def load_candidates_table_from_csv(self, path):
        """
        param path: a path to csv table with columns email, name, stage, status
        :return:
        """
        try:
            c = self.conn.cursor()
            df = pd.read_csv(fr'{path}')
            values = SqlServer._dataframe_to_database_values(df)

            query = "INSERT INTO Candidates(email, name, stage, status) VALUES {0};".format(values)
            c.execute(query)
        except Exception as e:
            print(e)
        finally:
            self.conn.commit()

    def add_grade(self, grade: Grade):
        c = self.conn.cursor()

        # need to add check that the grade.stage_id is at most the current stage of grade.candidate_email
        query = "INSERT INTO Grades(stage_id, candidate_email, score) VALUES ({0}, '{1}', {2});" \
            .format(grade.stage_id, grade.candidate_email, grade.score)

        c.execute(query)
        self.conn.commit()

    def add_candidate(self, candidate: Candidate):
        c = self.conn.cursor()
        query = "INSERT INTO Candidates(email, name, stage, status) VALUES ('{0}', '{1}', {2}, '{3}');" \
            .format(candidate.email, candidate.name, candidate.stage, candidate.status)

        c.execute(query)
        self.conn.commit()

    def get_all_candidates(self):
        c = self.conn.cursor()

        query = "SELECT email, name, stage FROM Candidates ORDER BY email"
        c.execute(query)
        df = pd.DataFrame(c.fetchall(), columns=['email', 'name', 'stage'])
        self.conn.commit()
        return SqlServer._candidates_df_to_jason(df=df)

    def get_candidates_at_stage(self, stage_id: int):
        c = self.conn.cursor()

        query = "SELECT email, name, stage FROM Candidates WHERE stage={0} ORDER BY email".format(stage_id)
        c.execute(query)
        df = pd.DataFrame(c.fetchall(), columns=['email', 'name', 'stage'])
        self.conn.commit()
        return SqlServer._candidates_df_to_jason(df=df)

    def get_candidates_query(self, condition: str = ""):
        c = self.conn.cursor()

        query = "SELECT email, name, stage FROM Candidates {0}".format(
            SqlServer._parse_candidate_condition(condition=condition))
        c.execute(query)
        df = pd.DataFrame(c.fetchall(), columns=['email', 'name', 'stage'])
        self.conn.commit()
        return SqlServer._candidates_df_to_jason(df=df)

    @staticmethod
    def _dataframe_to_database_values(df: pd.DataFrame):
        values = []
        column_headers = df.columns.values.tolist()
        for index in df.index:
            row = '('
            for column in column_headers:
                val = str(df[column][index]).strip()
                if not val.isnumeric() and val != 'True' and val != 'False':
                    # should be string type
                    row += f"'{val}', "
                else:
                    row += f"{val}, "
            row = row[:-2] + ")"
            values.append(row)

        res = ''
        for v in values[:-1]:
            res += f'{v}, '
        res += values[-1]
        return res

    @staticmethod
    def _parse_candidate_condition(condition: str):
        parse = condition.split(",")
        res = "WHERE "
        concat = " AND "
        error_cond = "WHERE FALSE"
        for cond in parse:
            d = list(filter(None, cond.split(" ")))
            if len(d) != 2:
                # bad condition
                res = error_cond
                break

            item1, item2 = d[0], d[1]
            key, val = SqlServer._get_key_val_candidate_condition(item1=item1, item2=item2)
            if not key or not val:
                # bad condition
                res = error_cond
                break
            if CANDIDATE_ENGLISH_COLS_TYPES[key] == "str":
                res += fr"{key}='{val}'" + concat
            elif CANDIDATE_ENGLISH_COLS_TYPES[key] == "int" or CANDIDATE_ENGLISH_COLS_TYPES[key] == "float":
                if not val.isnumeric():
                    # expect a numeric value
                    res = error_cond
                    break
                res += fr"{key}={val}" + concat
            else:
                res = error_cond

        ans = res
        if concat == res[-len(concat):]:
            ans = res[:-len(concat)]
        return ans

    @staticmethod
    def _get_key_val_candidate_condition(item1, item2):
        key, val = None, None
        if item1 in TRANSLATE_TO_ENGLISH.keys():
            key = TRANSLATE_TO_ENGLISH[item1]
            val = item2
        if item2 in TRANSLATE_TO_ENGLISH.keys():
            key = TRANSLATE_TO_ENGLISH[item2]
            val = item1
        return key, val

    @staticmethod
    def _candidates_df_to_jason(df):
        json = []
        for index, row in df.iterrows():
            email = row['email']
            name = row['name']
            stage = row['stage']

            d = {TRANSLATE_TO_HEBREW["email"]: fr"{email}",
                 TRANSLATE_TO_HEBREW["name"]: fr"{name}",
                 TRANSLATE_TO_HEBREW["stage"]: fr"{stage}"}
            json.append(d)
        return json

    def drop_tables(self):
        c = self.conn.cursor()
        query = "DROP TABLE IF EXISTS Grades;"
        c.execute(query)

        query = "DROP TABLE IF EXISTS Candidates;"
        c.execute(query)

        query = "DROP TABLE IF EXISTS Stages;"
        c.execute(query)
        self.conn.commit()

    def clear_tables(self):
        c = self.conn.cursor()

        query = "DELETE FROM TABLE EXISTS Grades;"
        c.execute(query)

        query = "DELETE FROM TABLE EXISTS Candidates;"
        c.execute(query)

        query = "DELETE FROM TABLE EXISTS Stages;"
        c.execute(query)
        self.conn.commit()


