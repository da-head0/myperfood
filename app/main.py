from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .library.helpers import *
from db.get_db import db, searchbytitle
from function.recommendation import compare_taste

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = "안녕하세요"
    # return templates.TemplateResponse("main.html", {"request": request, "data":data})

@app.get("/search/{title}", response_class=HTMLResponse)
async def bytitle(request: Request, title: str):
    data = searchbytitle(title)
    return templates.TemplateResponse("page.html", {"request": request, "data":data})


# @app.get("/id/{index}", response_class=HTMLResponse)
# async def searchbyid(request: Request, index: int):
#     data = searchbyid(index)
#     return templates.TemplateResponse("page.html", {"request": request, "data":data})

@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data":data})


@app.get("recommendation/{cat_id}", response_class=HTMLResponse)
async def recommend_food(request: Request, cat_id: int):
    data = compare_taste(cat_id)
    return templates.TemplateResponse("recommend.html", {"request": request, "data":data})

