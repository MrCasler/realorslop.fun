from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment
import json
from realorslop.services import gameplay
BASE_DIR = Path(__file__).resolve().parent.parent  # points to realorslop/


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/game", response_class=HTMLResponse)
def game_page(request: Request):
    game_data = gameplay.shuffle_pair()
    return templates.TemplateResponse("game.html", {"request": request, "game_data": game_data})
    
@app.get("/api/next", response_class=JSONResponse)
def api_next(request: Request):
    tag = request.query_params.get("tag")
    data = gameplay.shuffle_pair(tag)
    return JSONResponse(data)

@app.get("/api/tags")
def api_tags():
    tags = gameplay.get_tags()
    return {"tags": tags}