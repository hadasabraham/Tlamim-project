from pydantic import BaseModel


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
