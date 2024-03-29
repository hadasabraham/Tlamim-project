import datetime

from EmailServer import EmailServer
from FormsServer import FormServer
from Tables import Database, Candidate
from pathParameters.parameters import RegistrationFormParameter, StageParameter, FormParameter, StatusParameter, \
    GradeParameter, DecisionParameter, EmailParameter
from utils import search_candidates, set_registration_form, refresh_registration, reset_database, add_stage, add_form, \
    update_status, refresh_form, get_candidate_full_info, refresh_all_forms, add_grade, set_decision,send_email




def test_email(server: EmailServer):

    param = EmailParameter(to_email="halroy13@gmail.com", from_email="tlamin.group11@gmail.com",
                           subject=f"Test email at {datetime.datetime.now()}",
                           content="Welcome to Tlamim gmail server\r\n"
                                   "This email will be used to send updates about your application to Tlamim program\r\n")
    send_email(server=server, param=param)


def initial_test():
    form_id = "1wVJJhLn5Jaq3Dve-WhYwxt7nysmnSJISzzayRSypzS8"
    form_link = "https://docs.google.com/forms/d/e/1FAIpQLSd7tEnBxb6pUwTC70DgNHBEfl815LO0YxdaidBHk4I-ml2xog/viewform?usp=sf_link"

    server = FormServer(token_path="form_token.json", credentials_path="form_credentials.json")
    db = Database()
    reset_database(db=db)
    exit()
    set_registration_form(db=db, server=server, param=RegistrationFormParameter(form_id=form_id, form_link=form_link))

    try:
        add_stage(db=db, param=StageParameter(index=0, name="הרשמה ראשונית", msg=''))
        add_stage(db=db, param=StageParameter(index=1, name="היכרות", msg=''))
        add_stage(db=db, param=StageParameter(index=2, name="החלטת מוסד", msg=''))
        add_stage(db=db, param=StageParameter(index=3, name="התקבלות למסלול", msg=''))
    except Exception as e:
        print("Stage already exists")
        print(e)


    refresh_registration(db=db, server=server)

    try:
        form_id = "1oB-Uqee4MkneaouZLTn2VeljHUTgKCh6o93qKG1WJfU"
        form_link = "https://docs.google.com/forms/d/e/1FAIpQLScOOa8EoqZuo5cTTmEOr10j8dAIo9oF5umX--c2hdnVdVOdjQ/viewform?usp=sf_link"
        stage_index = 0
        add_form(db=db, server=server,
                 param=FormParameter(form_id=form_id, form_link=form_link, stage_index=stage_index))

        try:
            email = "avi@gmail.com"
            print("full info before refreshing", get_candidate_full_info(db=db, email=email))
        except Exception as e:
            print("Error full info")
            print(e)

        try:
            refresh_all_forms(db=db, server=server)
        except Exception as e:
            print("Refreshing form answers failed")
            print(e)

        try:
            email = "avi@gmail.com"
            print("full info after refreshing", get_candidate_full_info(db=db, email=email), end="\r\n\r\n")
        except Exception as e:
            print("Error full info")
            print(e)

    except Exception as e:
        print("Form already exists")
        print(e)

    try:
        email = "avi@gmail.com"
        print("full info before grade", get_candidate_full_info(db=db, email=email))
        add_grade(db=db, param=GradeParameter(email=email, stage=0, score=9, notes=''))
        print("full info after grade", get_candidate_full_info(db=db, email=email), end="\r\n\r\n")

    except Exception as e:
        print("Add grade error")
        print(e)


    try:
        email = "avi@gmail.com"
        param = "אימייל"
        condition = f"{param} = {email}"
        print(search_candidates(db=db, condition=condition))
    except Exception as e:
        print("Set search error")
        print(e)




    try:
        email = "avi@gmail.com"
        print("full info before decision", get_candidate_full_info(db=db, email=email))
        set_decision(db=db, param=DecisionParameter(email=email, stage=0, passed=True))
        print("full info after decision", get_candidate_full_info(db=db, email=email), end="\r\n\r\n")

    except Exception as e:
        print("Set decision error")
        print(e)


    try:
        reset_database(db=db)
    except Exception as e:
        print("Delete failed")
        print(e)


def main():
    email_server = EmailServer(token_path="gmail_token.json", credentials_path="credentials.json")
    test_email(server=email_server)





if __name__ == '__main__':
    main()
