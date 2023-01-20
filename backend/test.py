from BackendServer import BackendServer
from sql.entities.stage import Stage
from sql.entities.form import Form
from sql.entities.candidate import Candidate



def test(serve):

    stages = [Stage(stage_index=i, stage_name=f"{i}שלב ") for i in range(7)]

    forms = [Form(form_id="1K4v6Iyh9MWTu-4i3uYWtblb57wrwJC_hLnzYLk8UKtk",
                  form_link="https://docs.google.com/forms/d/e/1FAIpQLSelQPNkCQPGjJarUXqqdUaYByhb1wEQMQ3yBrhtJRC9IytnTQ/viewform?usp=sf_link",
                  stage_index=0)]

    candidates = [Candidate(email=f"candidate{i}@gmail.com",
                            first_name=f"first {i}",
                            last_name=f"last {i}") for i in range(10)]

    """
    for s in stages:
        serve.get_sql_server().add_stage(stage=s)
    for c in candidates:
        serve.get_sql_server().add_candidate(candidate=c)
    for f in forms:
        serve.get_sql_server().add_form(form=f)
    """


    serve.refresh_forms_answers()
    print(serve.get_candidate_entire_info(email="candidate0@gmail.com"))
    serve.save_snapshot(snapshot_name="snap0")


if __name__ == '__main__':
    server = BackendServer()
    test(serve=server)


