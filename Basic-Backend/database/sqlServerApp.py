import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.sqlserver import SqlServer
from database.candidate import Candidate
from database.stage import Stage

serverApp = FastAPI()

origins = ["*"]

serverApp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@serverApp.get("/candidates/query/", response_class=JSONResponse)
async def root(request: Request):
    response = JSONResponse([], headers={})
    return response


@serverApp.get("/candidates/query/{condition}", response_class=JSONResponse)
async def root(request: Request, condition: str):
    server = SqlServer()
    if condition == "הכול":
        json = server.get_all_candidates()
    else:
        json = server.get_candidates_query(condition)

    response = JSONResponse(json, headers={})
    return response


if __name__ == "__main__":

    """
    s = SqlServer()
    s.add_stage(stage=Stage(stage_id=1, form_link="form1"))
    s.add_stage(stage=Stage(stage_id=2, form_link="form2"))
    s.add_stage(stage=Stage(stage_id=3, form_link="form3"))
    s.add_stage(stage=Stage(stage_id=4, form_link="form4"))
    s.add_candidate(candidate=Candidate(email="moshe.56@gmail.com", name="משה", stage=1, status="לא הגיש"))
    s.add_candidate(candidate=Candidate(email="david56@gmail.com", name="דוד", stage=3, status="לא השלים"))
    s.add_candidate(candidate=Candidate(email="shlomi56@outlook.co.il", name="שלומי", stage=2, status="לא השלים"))
    s.add_candidate(candidate=Candidate(email="john56@gmail.com", name="יונתן", stage=2, status="ממתין לדירוג"))
    s.add_candidate(candidate=Candidate(email="niv23@outlook.com", name="ניב", stage=1, status="ממתין להחלטה"))
    s.add_candidate(candidate=Candidate(email="moshe1999@co.il", name="משה", stage=4, status="ממתין לדירוג"))
    """

    uvicorn.run("sqlServerApp:serverApp", host="127.0.0.1", port=8001)
