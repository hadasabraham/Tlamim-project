import json
from collections import defaultdict
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, MetaData, Table, Text, ForeignKey, \
    PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy import and_
from sqlalchemy import delete
import pymongo

from FormsServer import FormServer, FormDecoder

Base = declarative_base()


class Stage(Base):
    __tablename__ = "stages"

    index: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    msg: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return fr"Stage({self.index}, '{self.name}', '{self.msg}')"

    def __eq__(self, other):
        assert type(other) is Stage and self.index == other.index


class Candidate(Base):
    __tablename__ = "candidates"

    email: Mapped[str] = mapped_column(String, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    stage: Mapped[int] = mapped_column(Integer, ForeignKey("stages.index", ondelete="CASCADE"), nullable=False)
    modify: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return fr"Candidate('{self.email}', '{self.first_name}', '{self.last_name}', {self.stage}, {self.modify}, '{self.phone}', '{self.status}')"

    def __eq__(self, other):
        assert type(other) is Candidate and self.email == other.email


class Form(Base):
    __tablename__ = "forms"

    form_id: Mapped[str] = mapped_column('form_id', String, primary_key=True)
    form_link: Mapped[str] = mapped_column('form_link', String, nullable=False)
    stage: Mapped[int] = mapped_column(Integer, ForeignKey("stages.index", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return fr"Form('{self.form_id}', '{self.form_link}', {self.stage})"

    def __eq__(self, other):
        assert type(other) is Form and self.form_id == other.form_id


class Grade(Base):
    __tablename__ = "grades"
    email: Mapped[str] = mapped_column('email', String, ForeignKey('candidates.email', ondelete="CASCADE"),
                                       nullable=False, primary_key=True)
    stage: Mapped[int] = mapped_column('stage', Integer, ForeignKey('stages.index', ondelete="CASCADE"), nullable=False,
                                       primary_key=True)
    score: Mapped[int] = mapped_column('score', Integer, nullable=False)
    notes: Mapped[str] = mapped_column('notes', Text, nullable=True)

    def __repr__(self):
        return fr"Grade('{self.email}', {self.stage}, {self.score}, '{self.notes}')"

    def __eq__(self, other):
        assert type(other) is Grade and self.email == other.email and self.stage == other.stage


class Decision(Base):
    __tablename__ = "decisions"
    email: Mapped[str] = mapped_column('email', String, ForeignKey('grades.email', ondelete="CASCADE"),
                                       nullable=False, primary_key=True)
    stage: Mapped[int] = mapped_column('stage', Integer, ForeignKey('grades.stage', ondelete="CASCADE"), nullable=False,
                                       primary_key=True)
    passed: Mapped[bool] = mapped_column('passed', Boolean, nullable=False)

    def __repr__(self):
        return fr"Decision('{self.email}', {self.stage}, {self.passed})"

    def __eq__(self, other):
        assert type(other) is Decision and self.email == other.email and self.stage == other.stage


class FormsDatabase(object):

    def __init__(self, answers_db_name="answers_db"):
        self.client = pymongo.MongoClient()
        self.answers_db = self.client[answers_db_name]
        self.registration_form_collection = self.answers_db['registration']
        self.answers_form_structures = self.answers_db['structures']

    def add_form(self, form_id: str, form_structure: dict, last_update: str = None):
        self.answers_form_structures.insert_one(
            {
                "_id": form_id,
                "form_structure": form_structure,
                "last_update": last_update
            }
        )

    def get_form_structure_info(self, form_id: str):
        query = {"_id": form_id}
        return self.answers_form_structures.find_one(filter=query)

    def get_last_update(self, form_id: str) -> dict:
        query = {"_id": form_id}
        return self.answers_form_structures.find_one(filter=query, projection={"_id": False, "last_update": True})

    def add_answer(self, form_id: str, email: str, response: dict, last_update: str):
        answers = self.answers_db[form_id]
        exists = self.get_candidate_response(form_id=form_id, email=email)

        if not exists:
            document = {
                "_id": email,
                "response": response
            }
            answers.insert_one(
                document=document
            )
        else:
            query = {"_id": email}
            update = {'$set': {"response": response}}
            answers.find_one_and_update(filter=query, update=update)

            prev = self.get_last_update(form_id=form_id)['last_update']
            last_update = max(prev, last_update)

        self._refresh_last_update(form_id=form_id, last_update=last_update)

    def get_candidate_response(self, form_id: str, email: str) -> dict:
        query = {"_id": email}
        response = self.answers_db[form_id].find_one(filter=query, projection={"_id": False, "response": True})
        if response:
            if response is dict:
                response = response['response']
        return response

    def _refresh_last_update(self, form_id: str, last_update: str):
        query = {"_id": form_id}
        update = {'$set': {"last_update": last_update}}
        self.answers_form_structures.find_one_and_update(filter=query, update=update)

    def print_collections(self):
        print(self.answers_db.list_collection_names())

    def clear(self):
        for collection_name in self.answers_db.list_collection_names():
            collection = self.answers_db[collection_name]
            collection.delete_many({})

    def set_registration_form(self, form_id: str, form_link: str, form_structure: dict, last_update: str):
        if self.get_registration_form() is None:
            self.registration_form_collection.insert_one(
                {
                    "form_id": form_id,
                    "form_link": form_link,
                    "form_structure": form_structure,
                    "last_update": last_update
                }
            )

    def update_registration_last_update(self, last_update: str):
        r = self.get_registration_form()
        if r is not None:
            query = {"form_id": r['form_id']}
            update = {'$set': {"last_update": last_update}}
            self.registration_form_collection.find_one_and_update(filter=query, update=update)

    def get_registration_form(self):
        return self.registration_form_collection.find_one()


class Database(object):

    def __init__(self, db_name="database.db", echo=None):
        self.decisions = None
        self.grades = None
        self.candidates = None
        self.stages = None
        self.forms = None
        self.forms_db = FormsDatabase()
        self.meta = MetaData()
        self.engine = create_engine(f"sqlite:///{db_name}", echo=echo)
        # event.listen(self.engine, 'connect', Database._fk_pragma_on_connect)  # activate FK checkup

        self.session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.create_tables()

    def create_tables(self):
        self.stages = Table('stages', self.meta,
                            Column('index', Integer, primary_key=True),
                            Column('name', String, unique=True, nullable=False),
                            Column('msg', Text))

        self.candidates = Table('candidates', self.meta,
                                Column('email', String, primary_key=True),
                                Column('first_name', String, nullable=False),
                                Column('last_name', String, nullable=False),
                                Column('stage', Integer, ForeignKey('stages.index', ondelete="CASCADE"),
                                       nullable=False),
                                Column('modify', DateTime, nullable=False),
                                Column('phone', String, nullable=False, unique=True),
                                Column('status', String, nullable=True)
                                )

        self.forms = Table('forms', self.meta,
                           Column('form_id', String, primary_key=True),
                           Column('form_link', String, nullable=False, unique=True),
                           Column('stage', Integer, ForeignKey('stages.index', ondelete="CASCADE"), nullable=False)
                           )

        self.grades = Table('grades', self.meta,
                            Column('email', String, ForeignKey('candidates.email', ondelete="CASCADE"), nullable=False),
                            Column('stage', Integer, ForeignKey('stages.index', ondelete="CASCADE"), nullable=False),
                            Column('score', Integer, nullable=False),
                            Column('notes', Text, nullable=True),
                            PrimaryKeyConstraint('email', 'stage')
                            )

        self.decisions = Table('decisions', self.meta,
                               Column('email', String, ForeignKey('grades.email', ondelete="CASCADE"), nullable=False),
                               Column('stage', Integer, ForeignKey('grades.stage', ondelete="CASCADE"), nullable=False),
                               Column('passed', Boolean, nullable=False),
                               PrimaryKeyConstraint('email', 'stage')
                               )

        self.meta.create_all(self.engine)

    def clear_all(self):
        with self.session() as session:
            self.forms_db.clear()
            session.execute(delete(self.decisions))
            session.execute(delete(self.grades))
            session.execute(delete(self.forms))
            session.execute(delete(self.candidates))
            session.execute(delete(self.stages))
            session.commit()

    def set_decision(self, decision: Decision):
        next_stage_links = []
        with self.session() as session:
            candidate = session.query(Candidate).filter(Candidate.email == decision.email).first()
            exists = session.query(Decision).filter(Decision.stage == decision.stage,
                                                    Decision.email == decision.email).first()
            if not exists and candidate and decision.stage <= candidate.stage:
                session.add(decision)
            session.commit()

        if not exists and candidate and decision.stage <= candidate.stage and decision.passed:
            self.advance_candidate(email=decision.email)  # advance the candidate to the next stage if such exist

            # get the forms of the next stage that the candidate should fill
            forms = session.query(Form).filter(Form.stage == candidate.stage + 1).all()
            # if the next stage not exists there will be no forms to this stage
            for form in forms:
                next_stage_links.append(form.form_link)
        return next_stage_links

    def get_grades(self, email: str):
        with self.session() as session:
            grades = session.query(Grade).filter(Grade.email == email).order_by(Grade.stage).all()
            session.expunge_all()
            session.close()
        return grades

    def set_registration_form(self, form_id: str, form_link: str, form_structure: dict, last_update: str = None):
        self.forms_db.set_registration_form(form_id=form_id, form_link=form_link, form_structure=form_structure,
                                            last_update=last_update)

    def update_registration_form_last_update(self, last_update: str):
        self.forms_db.update_registration_last_update(last_update=last_update)

    def get_registration_form(self):
        return self.forms_db.get_registration_form()

    def is_candidate_exists(self, candidate: Candidate):
        with self.session() as session:
            exists = session.query(Candidate).filter(Candidate.email == candidate.email).first()
        if exists is None:
            return False
        return True

    def add_candidates(self, candidates: list[Candidate]):
        to_insert = []
        with self.session() as session:
            for candidate in candidates:
                if not self.is_candidate_exists(candidate=candidate):
                    to_insert.append(candidate)
            session.add_all(to_insert)
            session.commit()

    def add_candidate(self, candidate: Candidate):
        with self.session() as session:
            if not self.is_candidate_exists(candidate=candidate):
                session.add(candidate)
            session.commit()

    def update_status(self, email: str, status: str):
        with self.session() as session:
            session.query(Candidate).filter(Candidate.email == email).update(
                {
                    'status': status,
                    'modify': datetime.now()
                }
            )
            session.commit()

    def advance_candidate(self, email):
        next_index = self.get_next_stage(email=email)
        if next_index:
            with self.session() as session:
                session.query(Candidate).filter(Candidate.email == email).update(
                    {
                        'stage': next_index,
                        'modify': datetime.now()
                    }
                )
                session.commit()
            self.update_modify(email=email)

    def update_modify(self, email: str):
        with self.session() as session:
            session.query(Candidate).filter(Candidate.email == email).update(
                {'modify': datetime.now()}
            )
            session.commit()

    def search_candidates(self, condition: str):
        if not condition:
            with self.session() as session:
                res = session.query(Candidate)
                session.commit()
            return res
        parsed, succeed = Database._parse_condition(condition=condition)
        if not succeed:
            return []
        else:
            sql_conditions = []
            if parsed:
                for key, value in parsed:
                    if key == 'אימייל':
                        sql_conditions.append(Candidate.email.like(fr"{value}%"))
                    elif key == 'סטטוס':
                        sql_conditions.append(Candidate.status.like(fr"{value}%"))
                    elif key == 'טלפון':
                        sql_conditions.append(Candidate.phone.like(fr"{value}%"))
                    elif key == 'שם':
                        sql_conditions.append(
                            Candidate.first_name.concat(" ").concat(Candidate.last_name).like(fr"{value}%")
                        )
                    elif key == 'שלב':
                        sql_conditions.append(Candidate.stage == value)
                    elif key == 'תאריך':
                        sql_conditions.append(Candidate.modify == value)

            with self.session() as session:
                res = session.query(Candidate).filter(
                    Database._concat_condition_and(conditions=sql_conditions)).order_by(Candidate.modify)
            return res

    def is_stage_exists(self, stage: Stage):
        with self.session() as session:
            exists = session.query(Stage).filter(Stage.index == stage.index).first()
            session.commit()
        if exists is None:
            return False
        return True

    def add_grade(self, grade: Grade):
        with self.session() as session:
            exists = session.query(Grade).filter(
                Grade.email == grade.email, Grade.stage == grade.stage).first()
            if exists:
                if grade.score is not None:
                    session.query(Grade).filter(Grade.email == grade.email, Grade.stage == grade.stage).update({
                        'score': grade.score
                    })
                if grade.notes is not None:
                    session.query(Grade).filter(Grade.email == grade.email, Grade.stage == grade.stage).update({
                        'notes': grade.notes
                    })
            else:
                session.add(grade)
            session.commit()
        self.update_modify(email=grade.email)

    def add_stage(self, stage: Stage):
        with self.session() as session:
            if not self.is_stage_exists(stage=stage):
                session.add(stage)
            session.commit()

    def get_stages(self):
        with self.session() as session:
            stages = session.query(Stage).filter().order_by(Stage.index).all()
            session.expunge_all()
            session.close()
        return stages

    def get_next_stage(self, email: str):
        with self.session() as session:
            candidate = session.query(Candidate).filter(Candidate.email == email).first()
            next_index = min(session.query(Stage.index).filter(Stage.index > candidate.stage))[0]
            session.commit()
        return next_index

    def get_candidate(self, email) -> Candidate:
        with self.session() as session:
            candidate = session.query(Candidate).filter(Candidate.email == email).first()
            res = Candidate(email=candidate.email,
                            first_name=candidate.first_name,
                            last_name=candidate.last_name,
                            stage=candidate.stage,
                            modify=candidate.modify,
                            status=candidate.status,
                            phone=candidate.phone)
            session.commit()
        return res

    def is_form_exists(self, form: Form):
        with self.session() as session:
            res = session.query(Form).filter(Form.form_id == form.form_id).first()
        if res is None:
            return False
        return True

    def get_forms(self):
        with self.session() as session:
            res = session.query(Form)
            session.commit()
        return res

    def add_form(self, form: Form, form_structure: dict):
        """
        add form to the sql and add the structure to the mongodb
        :param form:
        :param form_structure:
        :return:
        """
        with self.session() as session:
            if not self.is_form_exists(form=form):
                session.add(form)
                self.forms_db.add_form(form_id=form.form_id, form_structure=form_structure)
            session.commit()

    def add_form_answer(self, form_id: str, form_response: dict):
        """
        add the answer to the mongodb and update the last_update (the max of the current and the form_response timestamp)
        :param form_id:
        :param form_response:
        :return:
        """

        timestamp = form_response['lastSubmittedTime']
        email = str(form_response['respondentEmail'])
        self.forms_db.add_answer(form_id=form_id, email=email, response=form_response, last_update=timestamp)

    def get_candidate_info(self, email: str):
        candidate = self.get_candidate(email=email)
        if candidate is None:
            return {}

        missing_forms = []
        answers_info = []
        grades_info = []
        notes = ""
        with self.session() as session:
            forms = session.query(Form).filter(Form.stage <= candidate.stage)

            forms_info = defaultdict(lambda: [])
            for form in forms:
                response = self.forms_db.get_candidate_response(form_id=form.form_id, email=email)
                if response:
                    form_structure = self.forms_db.get_form_structure_info(form_id=form.form_id)['form_structure']
                    q_a = FormDecoder.get_questions_answers(response=response['response'],
                                                            form_structure=form_structure)
                    for q, a in q_a:
                        forms_info[form.stage].append({'question': q, 'answer': a})
                else:
                    missing = {'stage': form.stage, 'form_id': form.form_id, 'form_link': form.form_link}
                    missing_forms.append(missing)

            grades = session.query(Grade).filter(
                Grade.email == candidate.email, Grade.stage <= candidate.stage).all()
            for grade in grades:
                grades_info.append({"stage": grade.stage, "score": grade.score, "notes": grade.notes})
                if grade.notes:
                    notes += grade.notes + "\r\n"

            for stage, info in forms_info.items():
                answers_info.append({"stage": stage, "answers": info})

            decision = session.query(Decision).filter(Decision.stage == candidate.stage,
                                                      Decision.email == candidate.email).first()
            session.commit()
        candidate_full = {'name': candidate.first_name + " " + candidate.last_name, 'email': candidate.email,
                          'current_stage': candidate.stage, 'status': candidate.status, 'phone': candidate.phone,
                          'modify': candidate.modify.strftime("%d/%m/%Y, %H:%M:%S"), 'answers': answers_info,
                          'grades': grades_info,
                          'missing': missing_forms,
                          'notes': notes,
                          'passed': decision.passed if decision else None}

        return candidate_full

    def export_candidates(self, condition: str, path: str):
        candidates = self.search_candidates(condition=condition)
        table = []
        for candidate in candidates:
            info = self.get_candidate_info(email=candidate.email)
            table.append(info)

        with open(path, "w") as copy:
            json.dump(table, copy)

    def get_form_structure_info(self, form_id: str):
        return self.forms_db.get_form_structure_info(form_id=form_id)

    def get_stages_info(self):
        forms_partition = defaultdict(lambda: [])
        res = []
        with self.session() as session:
            forms = session.query(Form)
            for form in forms:
                form_dict = {'link': form.form_link, 'id': form.form_id}
                forms_partition[form.stage].append(form_dict)

            stages = session.query(Stage).order_by(Stage.index)

            for stage in stages:
                stage_dict = {'index': stage.index, 'name': stage.name, 'msg': stage.msg, 'forms': forms_partition[stage.index]}
                res.append(stage_dict)
        return res



    @staticmethod
    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')  # when using sqlite need to explicitly check FK constraints

    @staticmethod
    def _concat_condition_and(conditions: list):
        res = conditions[0]
        for c in conditions[1:]:
            res = and_(c, res)
        return res

    @staticmethod
    def _parse_condition(condition):
        args = condition.split(',')
        parsed = []
        for pair in args:
            key_value = pair.split('=')
            if len(key_value) != 2:
                return parsed, False
            else:
                parsed.append((key_value[0].strip(), key_value[1].strip()))
        return parsed, True
