import time
from datetime import datetime

from BackendServer import BackendServer
from emails.EmailServer import EmailServer
from sql.SqlServer import SqlServer
from sql.entities.grade import Grade
from dateutil.parser import parse


def test(serve):
    """
        stages = [Stage(stage_index=i, stage_name=f"{i}שלב ") for i in range(7)]

    forms = [Form(form_id="1K4v6Iyh9MWTu-4i3uYWtblb57wrwJC_hLnzYLk8UKtk",
                  form_link="https://docs.google.com/forms/d/e/1FAIpQLSelQPNkCQPGjJarUXqqdUaYByhb1wEQMQ3yBrhtJRC9IytnTQ/viewform?usp=sf_link",
                  stage_index=0)]

    candidates = [Candidate(emails=f"candidate{i}@gmail.com",
                            first_name=f"first {i}",
                            last_name=f"last {i}",
                            timestamp=f"{datetime.now()}") for i in range(10)]

    for s in stages:
        serve.get_sql_server().add_stage(stage=s)
    for c in candidates:
        serve.get_sql_server().add_candidate(candidate=c)
    for f in forms:
        serve.get_sql_server().add_form(form=f)
    """
    serve.get_sql_server().load_snapshot(snapshot_name="snap0")

    # serve.refresh_forms_answers()
    print(serve.get_candidate_entire_info(email="candidate0@gmail.com"))
    """
    time.sleep(5)
    grade1 = Grade(emails="candidate0@gmail.com", stage_index=0, grade=10)
    serve.update_grade(grade=grade1)
    print(serve.get_candidate_entire_info(emails="candidate0@gmail.com"))

    # time.sleep(5)
    grade1 = Grade(emails="candidate0@gmail.com", stage_index=0, grade=None, passed=True, timestamp=f"{datetime.now()}")
    serve.update_grade(grade=grade1)
    print(serve.get_candidate_entire_info(emails="candidate0@gmail.com"))

    # time.sleep(5)
    grade1 = Grade(emails="candidate0@gmail.com", stage_index=0, grade=None, notes="איש מעניין מאוד")
    serve.update_grade(grade=grade1)
    print(serve.get_candidate_entire_info(emails="candidate0@gmail.com"))

    # time.sleep(5)
    grade1 = Grade(emails="candidate0@gmail.com", stage_index=0, grade=None, notes="איש מעניין מאוד")
    serve.update_grade(grade=grade1)
    print(serve.get_candidate_entire_info(emails="candidate0@gmail.com"))

    serve.advance_candidate(emails="candidate0@gmail.com")
    print(serve.get_candidate_entire_info(emails="candidate0@gmail.com"))

    # time.sleep(5)
    print("Here")
    grade1 = Grade(emails="candidate0@gmail.com", stage_index=1, grade=8, notes="מה קורה")
    serve.update_grade(grade=grade1)
    print(serve.get_candidate_entire_info(emails="candidate0@gmail.com"))
    """
    # serve.save_snapshot(snapshot_name="snap0")
    serve.get_sql_server().clear_tables()


if __name__ == '__main__':
    back = BackendServer()
    back.load_snapshot(snapshot_name="snap0")
    # back.add_stage(stage_index=1, stage_name="קורות חיים")
    # back.add_form(stage_index=1, form_id="10MfIxyz-UdkYJooKPiCU3u3uNHBiGcsgRxajHUNDhOU",
    #              form_link="https://docs.google.com/forms/d/e/1FAIpQLSeucoRDtIFtAsYYEZIqeSz3Dgx_4wP05bjDBpNiFefFQW8cRw/viewform?usp=sf_link")

    # back.refresh_registration_form()
    # back.refresh_forms_answers()

    print(back.get_stages_forms())
    print(back.get_candidate_entire_info(email="halroy13@gmail.com"))


    back.update_grade(Grade(email="halroy13@gmail.com", stage_index=0,
                            grade=5,
                            notes="אין"))

    print(back.get_candidate_entire_info(email="halroy13@gmail.com"))

    back.update_grade(Grade(email="halroy13@gmail.com", stage_index=0,
                            grade=9,
                            passed=True,
                            notes='שינוי בהתרשמות והוביל להעלאת הציון',
                            timestamp=f"{datetime.now()}"))

    print(back.get_candidate_entire_info(email="halroy13@gmail.com"))

    # back.save_snapshot(snapshot_name="snap0")
    back.get_sql_server().clear_tables()
    back.get_sql_server().drop_tables()



