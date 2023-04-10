from FormsServer import FormServer
from Tables import Database
from pathParameters.parameters import RegistrationFormParameter, StageParameter, FormParameter, StatusParameter, \
    GradeParameter, DecisionParameter
from utils import search_candidates, set_registration_form, refresh_registration, reset_database, add_stage, add_form, \
    update_status, refresh_form, get_candidate_full_info, refresh_all_forms, add_grade, set_decision


def main():
    form_id = "1wVJJhLn5Jaq3Dve-WhYwxt7nysmnSJISzzayRSypzS8"
    form_link = "https://docs.google.com/forms/d/e/1FAIpQLSd7tEnBxb6pUwTC70DgNHBEfl815LO0YxdaidBHk4I-ml2xog/viewform?usp=sf_link"

    server = FormServer(token_path="token.json", credentials_path="credentials.json")
    db = Database()
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
        print("full info before decision", get_candidate_full_info(db=db, email=email))
        set_decision(db=db, param=DecisionParameter(email=email, stage=0, passed=True))
        print("full info after decision", get_candidate_full_info(db=db, email=email), end="\r\n\r\n")

    except Exception as e:
        print("Set decision error")
        print(e)


    try:
        reset_database(db=db)
        pass
    except Exception as e:
        print("Delete failed")
        print(e)



if __name__ == '__main__':
    main()
