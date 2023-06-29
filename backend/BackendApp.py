import uvicorn
from fastapi import Body, FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from EmailServer import EmailServer
from FormsServer import FormServer
from pathParameters.parameters import *

from Tables import Database
import utils

serverApp = FastAPI()
db = Database()
formServer = FormServer(token_path="form_token.json", credentials_path="credentials.json")
emailServer = EmailServer(token_path="gmail_token.json", credentials_path="credentials.json")
utils.refresh_all_forms(db=db, server=formServer)

origins = ["*"]
serverApp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@serverApp.post("/clear")
async def clear(request: Request):
    utils.reset_database(db=db)


@serverApp.post("/export/")
async def export(export: ExportParameter = Body(embed=True)):
    db.export_candidates(export.condition, export.name)


@serverApp.post("/send/email")
async def send_email(email_parameter: EmailParameter = Body(embed=True)):
    utils.send_email(server=emailServer, param=email_parameter)


@serverApp.post("/set/status")
async def set_status(status_parameter: StatusParameter = Body(embed=True)):
    utils.update_status(db=db, param=status_parameter)
    

@serverApp.post("/set/general_notes")
async def set_general_notes(notes_parameter: GeneralNotesParameter = Body(embed=True)):
    utils.update_general_notes(db=db, param=notes_parameter)



@serverApp.post("/set/registration")
async def set_registration(registration_parameter: RegistrationFormParameter = Body(embed=True)):
    utils.set_registration_form(db=db, server=formServer, param=registration_parameter)


@serverApp.post("/refresh/registration")
async def refresh(request: Request):
    utils.refresh_registration(db=db, server=formServer)


@serverApp.post("/refresh/all")
async def refresh(request: Request):
    utils.refresh_all_forms(db=db, server=formServer)


@serverApp.post("/remove/stage/{stage}", response_class=JSONResponse)
async def remove_stage(stage: str):
    utils.remove_stage(db=db, stage=stage)


@serverApp.post("/add/stage")
async def add_stage(stage_parameter: StageParameter = Body(embed=True)):
    utils.add_stage(db=db, param=stage_parameter)


@serverApp.put("/add/form/")
async def add_form(form_parameter: FormParameter = Body(embed=True)):
    utils.add_form(db=db, server=formServer, param=form_parameter)


@serverApp.post("/set/grade")
async def set_grade(grade_parameter: GradeParameter = Body(embed=True)):
    utils.add_grade(db=db, param=grade_parameter)


@serverApp.post("/set/decision")
async def set_grade(decision_parameter: DecisionParameter = Body(embed=True)):
    next_stage_links = utils.set_decision(
        db=db, param=decision_parameter, email_serv=emailServer)
    # need to send mail with those links. and notify if passed



@serverApp.get("/candidates/search/{condition}", response_class=JSONResponse)
async def get_candidates(condition: str):
    candidates = utils.search_candidates(db=db, condition=condition)
    return JSONResponse(content=candidates)


@serverApp.get("/candidate/{email}", response_class=JSONResponse)
async def get_candidate(email: str):
    info = utils.get_candidate_full_info(db=db, email=email)
    return JSONResponse(content=info)


@serverApp.get("/stages", response_class=JSONResponse)
async def get_stages():
    info = utils.get_stages_info(db=db)
    return JSONResponse(content=info)


if __name__ == "__main__":
    uvicorn.run("BackendApp:serverApp", host="127.0.0.1", port=8001)
