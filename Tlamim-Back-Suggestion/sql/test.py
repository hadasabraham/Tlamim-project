import os
from sql.SqlServer import SqlServer
from sql.entities.form import Form
from sql.entities.generalQuestions import GeneralQuestions
from sql.entities.privateQuestions import PrivateQuestions

server = SqlServer()
server.drop_tables()
server.create_tables()
server.clear_tables()


def test1():
    base_path = fr"{os.getcwd()}\data\tables\xlsx"

    stages_table_path = fr"{base_path}\stagesTable.xlsx"
    server.load_stagesTable(path=stages_table_path, file_type="xlsx", hebrew_table=True)

    candidate_table_path = fr"{base_path}\candidatesTable.xlsx"
    server.load_candidatesTable(path=candidate_table_path, file_type="xlsx", hebrew_table=True)

    general_questions_table_path = fr"{base_path}\generalQuestionsTable.xlsx"
    server.load_generalQuestionsTable(path=general_questions_table_path, file_type="xlsx", hebrew_table=True)

    forms_table_path = fr"{base_path}\formsTable.xlsx"
    server.load_formsTable(path=forms_table_path, file_type="xlsx", hebrew_table=True)

    forms_answers_table_path = fr"{base_path}\formsAnswersTable.xlsx"
    server.load_formsAnswersTable(path=forms_answers_table_path, file_type="xlsx", hebrew_table=True)

    private_questions_table_path = fr"{base_path}\privateQuestionsTable.xlsx"
    server.load_privateQuestionsTable(path=private_questions_table_path, file_type="xlsx", hebrew_table=True)

    grades_table_path = fr"{base_path}\gradesTable.xlsx"
    server.load_gradesTable(path=grades_table_path, file_type="xlsx", hebrew_table=True)

    candidate0 = server.get_candidate_entire_info(email="candidate0@gmail.com")
    candidate1 = server.get_candidate_entire_info(email="candidate1@gmail.com")
    candidate2 = server.get_candidate_entire_info(email="candidate2@gmail.com")

    print("Candidate0")
    print(server.get_candidate_summarized(email="candidate0@gmail.com"))
    print(candidate0, end="\r\n\r\n")
    print("Candidate1")
    print(server.get_candidate_summarized(email="candidate1@gmail.com"))
    print(candidate1, end="\r\n\r\n")
    print("Candidate2")
    print(server.get_candidate_summarized(email="candidate2@gmail.com"))
    print(candidate2, end="\r\n\r\n")

    server.clear_tables()


def main():
    test1()
    server.drop_tables()


if __name__ == '__main__':
    main()
