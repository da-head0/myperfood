import os
from pymongo import MongoClient
import pprint
import requests
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
import re

host = 'cluster0.xc44g.mongodb.net'
user = 'aimb'
password = 'mimomimo'
database_name = 'cat'
collection = 'food'

client = MongoClient(f"mongodb+srv://{user}:{password}@{host}/{database_name}?retryWrites=true&w=majority")

db = client.cat
food_col = db.food
rating_col = db.rating
cat_col = db.user

class Rating(BaseModel):
    cat_id: int
    title : str
    rating : int

class User(BaseModel):
    cat_id: int
    cat_name : str
    cat_age : str

def searchbytitle(title):
    foodlist = []
    findfood = food_col.find({"title":{'$regex':f'.*{title}.*'}}) #{'title':title}
    for f in findfood:
        foodlist.append(f)
    return foodlist
    # for food in Food.objects:
    #     return food

def searchbyid(index):
    foodlist = []
    findfood = food_col.find({'index':index})
    for f in findfood:
        foodlist.append(f)
    return foodlist

def countcatnum():
    count = 0
    catlist = cat_col.find()
    for cat in catlist:
        count += 1
    return count + 1