from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from parameters import *
from BackendServer import BackendServer
from sql.entities.grade import Grade

serverApp = FastAPI()
backendServer = BackendServer()

origins = ["*"]
serverApp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@serverApp.post("/refresh_forms_answers")
async def refresh(request: Request):
    backendServer.refresh_registration_form()
    backendServer.refresh_forms_answers()


@serverApp.post("/snapshot")
async def save_snapshot(snapshot: SnapshotParameter):
    if snapshot.name is not None:
        backendServer.save_snapshot(snapshot_name=snapshot.name)


@serverApp.get("/snapshot{snapshot_name}")
async def load_snapshot(snapshot_name: str):
    if snapshot_name is not None:
        backendServer.load_snapshot(snapshot_name=snapshot_name)


@serverApp.put("/add/stage")
async def add_stage(stage_parameter: StageParameter):
    backendServer.add_stage(stage_index=stage_parameter.stage_index, stage_name=stage_parameter.stage_name)


@serverApp.put("/add/form")
async def add_stage(form_parameter: FormParameter):
    backendServer.add_form(stage_index=form_parameter.stage_index, form_id=form_parameter.form_id, form_link=form_parameter.form_link)


@serverApp.put("/update/grades")
async def update_grade(grade_parameter: GradeParameter):
    if grade_parameter.passed is None:
        grade = Grade(email=grade_parameter.email,
                      stage_index=grade_parameter.stage_index,
                      grade=grade_parameter.score,
                      passed=grade_parameter.passed,
                      notes=grade_parameter.notes)
    else:
        grade = Grade(email=grade_parameter.email,
                      stage_index=grade_parameter.stage_index,
                      grade=grade_parameter.score,
                      passed=grade_parameter.passed,
                      notes=grade_parameter.notes,
                      timestamp=f"{datetime.now()}")
    backendServer.update_grade(grade=grade)


@serverApp.put("/update/status")
async def update_status(dits: StatusParameter):
    backendServer.update_candidate_status(email=dits.email, status=dits.status)


@serverApp.get("/candidates/search/{condition}", response_class=JSONResponse)
async def search_candidates(condition: str):
    if not condition or condition == '':
        JSONResponse([], headers={})
    return JSONResponse(backendServer.search_candidates(condition=condition), headers={})


@serverApp.get("/candidate/entire_info/{email}", response_class=JSONResponse)
async def get_candidate_entire_info(email: str):
    return JSONResponse(backendServer.get_candidate_entire_info(email=email), headers={})


@serverApp.get("/candidate/summarized/{email}", response_class=JSONResponse)
async def get_candidate_summarized(email: str):
    return JSONResponse(backendServer.get_candidate_summarized(email=email), headers={})


if __name__ == "__main__":
    uvicorn.run("BackendApp:serverApp", host="127.0.0.1", port=8001)
