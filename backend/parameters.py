from pydantic import BaseModel


class SnapshotParameter(BaseModel):
    name: str
