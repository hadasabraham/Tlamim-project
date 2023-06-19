from datetime import datetime
from EmailServer import EmailServer
from FormsServer import FormServer, FormDecoder
from Tables import Database, Candidate, Stage, Form, Grade, Decision
from pathParameters.parameters import StageParameter, FormParameter, \
    RegistrationFormParameter, StatusParameter, GradeParameter, DecisionParameter, GeneralNotesParameter, EmailParameter


def reset_database(db: Database):
    db.clear_all()


def set_decision(db: Database, param: DecisionParameter, email_serv):
    decision = Decision(stage=param.stage, email=param.email, passed=param.passed)
    next_stage_links = db.set_decision(decision=decision)
    if param.passed:
        print("send", param.email, ",".join(next_stage_links))
        send_email(email_serv, EmailParameter(to_email="tlamin.group11@gmail.com",
                                              from_email="tlamin.group11@gmail.com",
                                              subject="שאלון תלמים", content=",".join(next_stage_links)))
    # EmailServer()
    return next_stage_links


def add_grade(db: Database, param: GradeParameter):
    grade = Grade(stage=param.stage, email=param.email, notes=param.notes, score=param.score)
    db.add_grade(grade=grade)
    db.update_average(email=param.email)  # after updating the grades of a candidate recalculate its average score


def add_stage(db: Database, param: StageParameter):
    stage = Stage(index=param.index, name=param.name, msg=param.msg)
    db.add_stage(stage=stage)


def add_form(db: Database, server: FormServer, param: FormParameter):
    if param.stage_index == "0":
        print("set registration form")
        set_registration_form(db=db, server=server,
                              param=RegistrationFormParameter(param.form_id, param.form_link))
    form = Form(form_id=param.form_id, form_link=param.form_link, stage=param.stage_index)
    form_structure = server.get_form_structure(form_id=param.form_id)
    db.add_form(form=form, form_structure=form_structure)


def search_candidates(db: Database, condition: str) -> list[dict]:
    res = []
    if condition == 'חסרים':
        for candidate in db.search_candidates(condition="הכול"):
            candidate_info = dict()
            candidate_info['name'] = candidate.first_name + " " + candidate.last_name
            candidate_info['email'] = candidate.email
            candidate_info['stage'] = candidate.stage
            candidate_info['status'] = candidate.status
            candidate_info['last_modify'] = candidate.modify.strftime(
                "%d/%m/%Y, %H:%M:%S")
            candidate_info['phone'] = candidate.phone
            candidate_info['missing'] = db.is_missing(candidate.email)
            candidate_info['general_notes'] = candidate.general_notes
            candidate_info['average_grade'] = candidate.average_grade
            if db.is_missing(candidate.email):
                res.append(candidate_info)
        return res
    for candidate in db.search_candidates(condition=condition):
        candidate_info = dict()
        candidate_info['name'] = candidate.first_name + " " + candidate.last_name
        candidate_info['email'] = candidate.email
        candidate_info['stage'] = candidate.stage
        candidate_info['status'] = candidate.status
        candidate_info['last_modify'] = candidate.modify.strftime("%d/%m/%Y, %H:%M:%S")
        candidate_info['phone'] = candidate.phone
        candidate_info['missing'] = db.is_missing(candidate.email)
        candidate_info['general_notes'] = candidate.general_notes
        candidate_info['average_grade'] = candidate.average_grade
        res.append(candidate_info)
    res = sorted(sorted(res, key=lambda e: e['name']), key=lambda e: (not e['missing']))
    return res


def refresh_registration(db: Database, server: FormServer):
    registration_form = db.get_registration_form()

    original_last_response = ""
    if registration_form:
        form_id = registration_form['form_id']
    else:
        return

    if "last_response" in registration_form.keys():
        original_last_response = registration_form['last_response']

    form_structure = registration_form['form_structure']  # later save in the db and load from there

    responses = server.get_form_responses(form_id=form_id, last_response=original_last_response)
    last_response = original_last_response
    if responses:
        candidates = []
        for response in responses['responses']:
            questions = FormDecoder.get_form_questions(form_structure=form_structure)
            email_qid = FormDecoder.get_key_qid(form_structure=form_structure)
            email, timestamp, answers = FormDecoder.get_form_answers(response=response, email_qid=email_qid)

            q_a = FormDecoder.match(form_questions=questions, form_answers=answers)
            first_name, last_name, stage, modify, phone, status = None, None, 0, datetime.now(), None, "חדש"
            for q_title, q_ans in q_a:
                if q_title == "שם פרטי" or q_title == "שם  פרטי":
                    first_name = q_ans
                elif q_title == "שם משפחה":
                    last_name = q_ans
                elif q_title == "טלפון":
                    phone = q_ans

            candidate = Candidate(email=email,
                                  first_name=first_name,
                                  last_name=last_name,
                                  stage=stage,
                                  modify=modify,
                                  phone=phone,
                                  status=status)
            candidates.append(candidate)

            if last_response is not None:
                last_response = max(last_response, timestamp)
            else:
                last_response = timestamp

        if last_response is not None:
            if original_last_response is None or last_response > original_last_response:
                db.update_registration_form_last_update(last_update=last_response)

        try:
            db.add_candidates(candidates=candidates)
        except Exception as e:
            print("Candidates already exists")


def refresh_form(db: Database, server: FormServer, form_id: str):
    form_info = db.get_form_structure_info(form_id=form_id)
    last_update = ""
    if not form_info:
        return

    if "last_update" in form_info.keys():
        last_update = form_info['last_update']

    responses = server.get_form_responses(form_id=form_id, last_response=last_update)
    form_structure = db.get_form_structure_info(form_id=form_id)[
        'form_structure']
    email_qid = FormDecoder.get_key_qid(form_structure=form_structure)
    if responses:
        for response in responses['responses']:
            # "last update" updates automatically after each response addition
            db.add_form_answer(form_id=form_id, form_response=response, email_qid=email_qid)


def refresh_all_forms(db: Database, server: FormServer):
    refresh_registration(db=db, server=server)
    forms = db.get_forms()
    for form in forms:
        refresh_form(db=db, server=server, form_id=form.form_id)


def get_candidate_full_info(db: Database, email: str):
    res = db.get_candidate_info(email=email)
    return res


def set_registration_form(db: Database, server: FormServer, param: RegistrationFormParameter):
    form_structure = server.get_form_structure(form_id=param.form_id)
    db.set_registration_form(form_id=param.form_id, form_link=param.form_link, form_structure=form_structure)


def update_status(db: Database, param: StatusParameter):
    db.update_status(email=param.email, status=param.status)


def update_general_notes(db: Database, param: GeneralNotesParameter):
    db.update_general_notes(email=param.email, general_notes=param.notes)


def get_stages_info(db: Database):
    return db.get_stages_info()


def send_email(server: EmailServer, param=EmailParameter):
    server.send_email(to_email=param.to_email, from_email=param.from_email, subject=param.subject, content=param.content)
