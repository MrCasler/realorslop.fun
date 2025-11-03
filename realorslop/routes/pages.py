from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment
import json
from services import gameplay
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/game", response_class=HTMLResponse)
def game_page(request: Request):
    game_data = gameplay.shuffle_pair()
    return templates.TemplateResponse("game.html", {"request": request, "game_data": game_data})