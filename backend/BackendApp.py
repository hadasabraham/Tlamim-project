import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from BackendServer import BackendServer
from pathParameters.parameters import *

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
    backendServer.refresh_forms_answers()


@serverApp.get("/candidates/search", response_class=JSONResponse)
async def search_candidates(request: Request, query: ConditionParameter):
    if not query.condition or query.condition == '':
        JSONResponse([], headers={})
    return JSONResponse(backendServer.search_candidates(condition=query.condition), headers={})


@serverApp.get("/candidate/entire_info", response_class=JSONResponse)
async def get_candidate_entire_info(request: Request, query: EmailParameter):
    return JSONResponse(backendServer.get_candidate_entire_info(email=query.email), headers={})


@serverApp.get("/candidate/summarized", response_class=JSONResponse)
async def get_candidate_summarized(request: Request, query: EmailParameter):
    return JSONResponse(backendServer.get_candidate_summarized(email=query.email), headers={})


if __name__ == "__main__":
    uvicorn.run("BackendApp:serverApp", host="127.0.0.1", port=8001)
