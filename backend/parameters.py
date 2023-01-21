from pydantic import BaseModel


class PromoteCandidate(BaseModel):
    email: str


class StageParameter(BaseModel):
    stage_index: int
    stage_name: str


class FormParameter(BaseModel):
    stage_index: int
    form_id: str
    form_link: str


class SnapshotParameter(BaseModel):
    name: str


class StatusParameter(BaseModel):
    email: str
    status: str


class GradeParameter(BaseModel):
    email: str
    stage_index: int
    score: float | None
    notes: str | None
    passed: bool | None
