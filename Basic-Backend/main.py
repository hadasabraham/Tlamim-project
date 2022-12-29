import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='template')


@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('basic.html', {"request": request})


@app.get("/mail")
async def root(request: Request):
    return templates.TemplateResponse('mail.html', {"request": request})


@app.get("/data/candidate")
async def root(request: Request):
    return templates.TemplateResponse('candidate.html', {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
