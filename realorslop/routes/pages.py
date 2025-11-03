from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment
import json
from realorslop.services import gameplay
BASE_DIR = Path(__file__).resolve().parent.parent  # points to realorslop/


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

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