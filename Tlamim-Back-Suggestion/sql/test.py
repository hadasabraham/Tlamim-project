import pandas as pd

from sql.SqlServer import SqlServer
from sql.entities.stage import Stage
from sql.entities.table import *
from sql.entities.candidate import Candidate
from sql.entities.form import Form

server = SqlServer()
server.create_tables()
server.clear_tables()


def test_add_stages(num_of_stages: int, clear: bool = True, suppress_prints: bool = True):
    stages = []

    if clear:
        server.clear_tables()

    for i in range(num_of_stages):
        stg = Stage(stage_index=i, stage_name=f"stage number {i}")
        stages.append([stg.index, stg.name])
        server.add_stage(stage=stg)

    eng_columns = [eng for eng, _, _ in StagesTable.get_sql_cols()]
    correct = pd.DataFrame(stages, columns=eng_columns)
    actual = server.get_stagesTable()

    if not suppress_prints:
        print("Correct")
        print(correct, end="\r\n\r\n")
        print("Actual")
        print(actual, end="\r\n\r\n")

    assert actual.equals(correct)

    if clear:
        server.clear_tables()


def test_load_stages(xlsx_file_name: str, csv_file_name: str, suppress_prints: bool = True, clear: bool = True):
    xlsx_path = fr"C:\Users\halro\Desktop\Tlamim-project\Tlamim-Back-Suggestion\sql\xlsx\{xlsx_file_name}"
    csv_path = fr"C:\Users\halro\Desktop\Tlamim-project\Tlamim-Back-Suggestion\sql\csv\{csv_file_name}"

    server.load_stagesTable(path=xlsx_path, file_type='xlsx', hebrew_table=False)
    xlsx_stages = server.get_stagesTable()
    if not suppress_prints:
        print("xlsx Stages Table")
        print(xlsx_stages, end="\r\n\r\n")

    server.clear_tables()

    server.load_stagesTable(path=csv_path, file_type='csv', hebrew_table=False)
    csv_stages = server.get_stagesTable()
    if not suppress_prints:
        print("csv Stages Table")
        print(csv_stages, end="\r\n\r\n")

    if clear:
        server.clear_tables()


def test_export_stages(xlsx_file_name: str, csv_file_name: str, index: bool, clear: bool = True):
    xlsx_path = fr"C:\Users\halro\Desktop\Tlamim-project\Tlamim-Back-Suggestion\sql\xlsx\{xlsx_file_name}"
    csv_path = fr"C:\Users\halro\Desktop\Tlamim-project\Tlamim-Back-Suggestion\sql\csv\{csv_file_name}"

    test_add_stages(num_of_stages=10, clear=False)

    server.export_stagesTable(path=xlsx_path, file_type='xlsx', index=index)
    server.export_stagesTable(path=csv_path, file_type='csv', index=index)

    if clear:
        server.clear_tables()


def test_add_candidates(num_of_stages: int, candidates_per_stage: int, clear: bool = True):
    candidates = []

    test_add_stages(num_of_stages=num_of_stages, clear=False)
    for i in range(num_of_stages):
        for j in range(candidates_per_stage):
            can = Candidate(email=f"candidate.stage{i}.candidate{j}", first_name=f"first s{i}n{j}",
                            last_name=f"last s{i}n{j}", stage_index=i)
            server.add_candidate(candidate=can)
            candidates.append((can.email, can.first_name, can.last_name, can.stage_index, can.status))
    eng_columns = [eng for eng, _, _ in CandidatesTable.get_sql_cols()]
    correct = pd.DataFrame(candidates, columns=eng_columns)
    actual = server.get_candidatesTable()
    if clear:
        server.clear_tables()

    assert actual.equals(correct)


def test1():
    stages = [Stage(stage_index=i, stage_name=f"{i}שלב מספר ") for i in range(10)]
    candidates = []
    for stage in stages:
        for i in range(10):
            can = Candidate(email=f"email.stage{stage.index}.candidate{i}@gmail.com",
                            first_name=f"{stage.index * 10 + i}שם פרטי ",
                            last_name=f"{stage.index * 10 + i}שם משפחה ",
                            stage_index=stage.index)
            candidates.append(can)

    forms = []
    for stage in stages:
        for i in range(2):
            form = Form(form_id=f"form id {stage.index * 2 + i}",
                        form_link=f"form link {stage.index * 2 + i}",
                        stage_index=stage.index)
            forms.append(form)

    for stage in stages:
        server.add_stage(stage=stage)
    for form in forms:
        server.add_form(form=form)
    for candidate in candidates:
        server.add_candidate(candidate=candidate)

    actual_stages = server.get_stagesTable()
    actual_candidates = server.get_candidatesTable()
    actual_forms = server.get_formsTable()

    # print(actual_stages['stage_name'], end="\r\n\r\n")

    # print(actual_candidates['first_name'], end="\r\n\r\n")
    # print(actual_candidates['last_name'], end="\r\n\r\n")

    # print(actual_forms['responses_file_path'], end="\r\n\r\n")

    candidate_to_get = Candidate(email="halroy13@gmail.com", first_name="רוי", last_name="הלחמי")
    server.add_candidate(candidate_to_get)

    print(server.get_candidate(email="halroy13@gmail.com"), end="\r\n\r\n")

    row = Table.find_row(path=fr"C:\Users\halro\Desktop\Tlamim-project\Tlamim-Back-Suggestion\sql\xlsx\test.xlsx",
                         file_type="xlsx",
                         english_key="email",
                         hebrew_key='דוא"ל', value="halroy13@gmail.com")

    print(row, end="\r\n\r\n")

    print("Search row")
    row = Table.get_row(path=fr"C:\Users\halro\Desktop\Tlamim-project\Tlamim-Back-Suggestion\sql\xlsx\test.xlsx",
                        file_type="xlsx", row_index=1)
    print(row, end="\r\n\r\n")

    print("Row to json")
    print(Table.get_row_as_json_list(
        path=fr"C:\Users\halro\Desktop\Tlamim-project\Tlamim-Back-Suggestion\sql\xlsx\test.xlsx",
        file_type="xlsx", row_index=1))

    print(Table.row_to_json_list(row=row))

    server.clear_tables()


def main():
    test_add_candidates(num_of_stages=10, candidates_per_stage=10)
    test1()
    server.drop_tables()


if __name__ == '__main__':
    main()
