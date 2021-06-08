from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from db.get_db import db, food_col, cat_col, searchbytitle, countcatnum
from function.recommendation import compare_taste
import uvicorn
from starlette.responses import RedirectResponse


app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/main", response_class=HTMLResponse)
async def home(request: Request):
    datalist = []
    data = food_col.find()
    for d in data:
        datalist.append(d) 
    return templates.TemplateResponse("page.html", {"request": request, "data":datalist})

# @app.post("/main", response_class=HTMLResponse)
# async def rating(request: Request, radio1 : str):
#     datalist = []
#     data = food_col.find()
#     for d in data:
#         datalist.append(d)
#     if radio1:
#         return templates.TemplateResponse("page.html", {"request": request, "data":data, "star" : radio1})


@app.get("/recommendation", response_class=HTMLResponse)
async def recommend_food(request: Request, cat_id: int=1.0):
    datalist = compare_taste(cat_id)
    findlist = []
    catratedlist = []
    # 이미 고양이가 평가한 리스트 만들기
    catrated = cat_col.find({'cat_id':cat_id})
    for cat in catrated:
        catratedlist.append(cat['title'])
    for d in datalist:
        # 이미 고양이가 평가한것은 제외
        if d in catratedlist:
            pass
        else:
            # d가 이미 고른 타이틀이 아닌지 확인 필요
            findfood = food_col.find({'index':d}) #{'title':title}
            for f in findfood:
                findlist.append(f)
    return templates.TemplateResponse("recommend.html", {"request": request, "data":findlist})

# @app.get("/", response_class=HTMLResponse)
# async def userinfo(request: Request, catname : str = Form(...), catage : str = Form(...)):
#     data = "어떤 고양이를 키우시나요?"
#     catindex = countcatnum()
#     cat_col.insert_one("cat_id":catindex, "cat_name":catname, "cat_age":catage)
#     return templates.TemplateResponse("user.html", {"request": request, "data":data})

@app.get("/mainsearch/", response_class=HTMLResponse)
async def bytitle(request: Request, search_name: str):
    if search_name:
        data = searchbytitle(search_name)
        return templates.TemplateResponse("page.html", {"request": request, "data":data})
    #url = f'http://127.0.0.1:8000/search?{searchtitle}'

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
