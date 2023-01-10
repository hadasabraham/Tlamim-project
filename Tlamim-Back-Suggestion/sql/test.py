import random
from operator import itemgetter
import numpy as np
import pandas as pd

from SqlServer import *


def add_stages(server: SqlServer):
    stages = [Stage(stage_index=i, stage_name=f"stage {i}") for i in range(10)]

    eng_col = [eng for eng, _, _ in Stage.get_attributes_info()]
    tmp = []
    for stage in stages:
        tmp.append([stage.index, stage.name])
    correct = pd.DataFrame(tmp, columns=eng_col)

    for stage in stages:
        server.add_stage(stage=stage)

    actual = server.get_stages()
    assert actual.equals(correct)


def add_stages_with_default_forms(server: SqlServer):
    stages = [Stage(stage_index=i, stage_name=f"stage {i}") for i in range(10)]

    eng_col = [eng for eng, _, _ in Stage.get_attributes_info()]
    tmp = []

    forms = []
    for stage in stages:
        stage.add_form(form_id=f"form {stage.name}", form_link=f"link form {stage.name}")
        tmp.append([stage.index, stage.name])
        forms.append([stage.index, f"form {stage.name}", f"link form {stage.name}"])
    correct = pd.DataFrame(tmp, columns=eng_col)

    for stage in stages:
        server.add_stage(stage=stage)

    actual = server.get_stages()
    assert actual.equals(correct)

    eng_col = [eng for eng, _, _ in Form.get_attributes_info()]
    forms_correct = pd.DataFrame(forms, columns=eng_col)

    forms_actual = server.get_forms()

    assert forms_actual.equals(forms_correct)
    return stages


def add_candidate(server: SqlServer):
    stages = add_stages_with_default_forms(server=server)

    last_stage = max([stage.index for stage in stages])

    ret = []
    candidates = []
    for stage in stages:
        for i in range(10):
            candidate = Candidate(email=f"candidate.email.{stage.index}.{i}@gmail.com",
                                  first_name=f"first{stage.index}{i}",
                                  last_name=f"last{stage.name}{i}",
                                  stage_index=random.randint(0, last_stage))
            server.add_candidate(candidate=candidate)
            ret.append(candidate)
            candidates.append(
                [candidate.email, candidate.first_name, candidate.last_name, candidate.stage_index, candidate.status])

    eng_col = [eng for eng, _, _ in Candidate.get_attributes_info()]
    correct = pd.DataFrame(candidates, columns=eng_col)
    actual = server.get_candidates()

    assert actual.equals(correct)
    return ret


def add_grades(server: SqlServer):
    candidates = add_candidate(server=server)

    correct = []
    for candidate in candidates:
        g = Grade(stage=candidate.stage_index,
                  grade=float(random.uniform(0, 10), ),
                  notes=[f"note on {candidate.first_name}"],
                  passed=[True, False][random.randint(0, 1)])

        server.add_grade(candidate_email=candidate.email, grade=g)
        correct.append([g.stage, candidate.email, g.grade, g.get_notes_str(), g.passed])

    correct = sorted(correct, key=itemgetter(1))
    eng_col = [eng for eng, _, _ in Grade.get_attributes_info()]
    correct = pd.DataFrame(correct, columns=eng_col)

    actual = server.get_grades()

    print(actual.compare(correct))  # if the different only on grade column with small margin its ok (comparing floats can be problematic)


def main():
    server = SqlServer()

    server.create_tables()

    add_grades(server=server)

    server.drop_tables()


if __name__ == '__main__':
    main()
