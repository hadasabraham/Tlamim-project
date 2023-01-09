import sqlite3 as sql
import pandas as pd


class SqlServer(object):

    def __init__(self, database='test_database'):
        self.__conn = sql.connect(database=database)

    def create_tables(self):
        pass

    def drop_tables(self):
        pass

    def clear_table(self):
        pass

    def get_candidates_general_information(self, condition: str):
        """

        :param condition: condition only on the general information attributes
        :return:
        """
        pass

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
    
    
    CandidatesGeneralInformation(email TEXT PRIMARY KEY, first_name TEXT NOT NULL, family_name TEXT NOT NULL,
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
