from pydantic.dataclasses import dataclass

@dataclass
class FormParameter:
    form_id: str
    form_link: str
    stage_index: str

    def __init__(self, form_id: str, form_link: str, stage_index: str):
        self.form_id = form_id
        self.form_link = form_link
        self.stage_index = stage_index


@dataclass
class RegistrationFormParameter:
    form_id: str
    form_link: str

    def __init__(self, form_id: str, form_link: str):
        self.form_id = form_id
        self.form_link = form_link


@dataclass
class StatusParameter:
    email: str
    status: str

    def __init__(self, email: str, status: str):
        self.email = email
        self.status = status


@dataclass
class StageParameter:
    index: str
    name: str
    msg: str

    def __init__(self, index: str, name: str, msg: str):
        self.index = index
        self.name = name
        self.msg = msg


@dataclass
class GradeParameter:
    stage: int
    email: str
    score: int
    notes: str

    def __init__(self, stage: int, email: str, score: int, notes: str):
        self.stage = stage
        self.email = email
        self.score = score
        self.notes = notes


@dataclass
class DecisionParameter:
    stage: int
    email: str
    passed: bool

    def __init__(self, stage: int, email: str, passed: bool):
        self.stage = stage
        self.email = email
        self.passed = passed

@dataclass
class ExportParameter:
    name: str
    
    def __init__(self, name: str):
        self.name = name
