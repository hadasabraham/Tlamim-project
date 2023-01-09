import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from BackendServer import BackendServer

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
    pass


@serverApp.get("/candidates/query/{condition}", response_class=JSONResponse)
async def root(request: Request, condition: str):
    pass


if __name__ == "__main__":

    uvicorn.run("BackendApp:serverApp", host="127.0.0.1", port=8001)
