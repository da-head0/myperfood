from fastapi import FastAPI, Request, Form, status, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from db.get_db import db, food_col, rating_col, cat_col, searchbytitle, countcatnum, Rating, User
from function.recommendation import compare_taste
import uvicorn
from starlette.responses import RedirectResponse
from starlette.requests import Request



app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def userinfo(request: Request, catname : str=None, catage : str=None):
    data = "어떤 고양이를 키우시나요?"
    catindex = countcatnum()
    existcat = rating_col.find_one({"cat_name":catname}) 
    if not existcat:
        cat_col.insert_one({"cat_id":catindex, "cat_name":catname, "cat_age":catage})
        message = "유저 정보가 등록되었습니다!"
        return templates.TemplateResponse("user.html", {"request": request, "data":data, "message" : message})
    else: # 고양이를 중복 입력할 경우
        # 이부분 안됨.. 왜 안될까..!
        cat_col.update({"cat_id":catindex-1}, {"$set" : {"cat_name":catname, "cat_age":catage}})
    return templates.TemplateResponse("user.html", {"request": request, "data":data})

# @app.get("/main", response_class=HTMLResponse)
# async def home(request: Request):
#     datalist = []
#     data = food_col.find()
#     for d in data:
#         datalist.append(d) 
#     return templates.TemplateResponse("page.html", {"request": request, "data":datalist})
from pydantic import BaseModel

class FoodItem(BaseModel):
    title: str

# @app.get("/main", response_class=HTMLResponse)
# async def rating(request: Request):
#     #data = "고양이가 좋아하는 사료, 싫어하는 사료를 체크해 보세요"
#     datalist = []
#     data = food_col.find()
#     for d in data:
#         datalist.append(d)
#     return templates.TemplateResponse("page.html", {"request": request, "data":datalist})

@app.get("/main", response_class=HTMLResponse)
async def rating(request: Request,foodtitle: str = None, stars : int=None):
    data = "고양이가 좋아하는 사료, 싫어하는 사료를 체크해 보세요"
    datalist = []
    data = food_col.find()
    for d in data:
        datalist.append(d)
    if stars:
        foodtitle = foodtitle
        catindex = countcatnum() # 일단.. 가장 이전 유저로 한다. 바꿔야 함.
        existitem = rating_col.find_one({"cat_id":catindex, "title":foodtitle}) 
        if not existitem:
            rating_col.insert_one({"cat_id":catindex, "title":foodtitle, "rating":stars})
            message = "선호 정보가 등록되었습니다"
            return templates.TemplateResponse("page.html", {"request": request, "data":datalist, "message" : message})
        else:
            rating_col.update_one({"cat_id":catindex, "title":foodtitle}, {"$set" : {"rating":stars}})
    return templates.TemplateResponse("page.html", {"request": request, "data":datalist})

@app.get("/recommendation", response_class=HTMLResponse)
async def recommend_food(request: Request, cat_id: int=1.0):
    tastecompared = compare_taste(cat_id) # 인덱스 숫자가 옴
    findlist = []
    catratedlist = []
    # 이미 고양이가 평가한 리스트 만들기
    catrated = rating_col.find({'cat_id':cat_id})
    for cat in catrated:
        catratedlist.append(cat['title']) # 평가한 리스트
    for d in tastecompared:
        findfood = food_col.find({'index':d}) # 개별 정보
        # 이미 고양이가 평가한것은 제외
        for f in findfood: # fast api에서는 이렇게 조건문으로 해주어야 한다... 빼면 오류남
            if f['title'] in catratedlist:
                pass
            else:
            # d가 이미 고른 타이틀이 아닌지 확인 필요
                findlist.append(f)
    return templates.TemplateResponse("recommend.html", {"cat": cat_col.find_one({"cat_id":cat_id}), "request": request, "data":findlist})

@app.get("/catinfo", response_class=HTMLResponse)
async def recommend_food(request: Request, cat_id: int=1.0):
    catlist = []
    cats = cat_col.find()
    for cat in cats:
        catlist.append(cat)
    return templates.TemplateResponse("catinfo.html", {"request": request, "cats":catlist})

@app.get("/search/{title}", response_class=HTMLResponse)
async def bytitle(request: Request, title: str):
    data = searchbytitle(title)
    return templates.TemplateResponse("page.html", {"request": request, "data":data})
