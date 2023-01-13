import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from BackendServer import BackendServer

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


@serverApp.get("/candidates/query/", response_class=JSONResponse)
async def root(request: Request):
    response = JSONResponse([], headers={})
    return response


@serverApp.get("/candidates/query/{condition}", response_class=JSONResponse)
async def search_candidates(request: Request, condition: str):
    return JSONResponse(backendServer.search_candidates(condition=condition), headers={})


@serverApp.get("/candidate/entire_info/{email}", response_class=JSONResponse)
async def get_candidate_entire_info(request: Request, email: str):
    return JSONResponse(backendServer.get_candidate_entire_info(email=email), headers={})


@serverApp.get("/candidate/entire_info/{email}", response_class=JSONResponse)
async def get_candidate_summarized(request: Request, email: str):
    return JSONResponse(backendServer.get_candidate_summarized(email=email), headers={})


if __name__ == "__main__":
    uvicorn.run("BackendApp:serverApp", host="127.0.0.1", port=8001)
