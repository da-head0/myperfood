import os
from pymongo import MongoClient
import pprint
import requests
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

host = 'cluster0.xc44g.mongodb.net'
user = 'aimb'
password = 'mimomimo'
database_name = 'cat'
collection = 'food'

client = MongoClient(f"mongodb+srv://{user}:{password}@{host}/{database_name}?retryWrites=true&w=majority")

db = client.cat


# class PyObjectId(ObjectId):

#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError('Invalid objectid')
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type='string')

# class Food(BaseModel):
#     id: Optional[PyObjectId] = Field(alias='_id')
#     uuid : str
#     category : str
#     brand : str
#     title : str
#     age : str
#     classification : str
#     content : str
#     nutrient : str
#     info : str
#     gram : str
#     calory : str
#     ingredient : str
#     detail : str
#     from_company : str
#     성분등록번호 : str
#     img : str

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {
#             ObjectId: str
#         }

# class Food(Document):
#     uuid = StringField()
#     category = StringField()
#     brand = StringField()
#     title = StringField()
#     age = StringField()
#     classification = StringField()
#     content = StringField()
#     nutrient = StringField()
#     info = StringField()
#     gram = StringField()
#     calory = StringField()
#     ingredient = StringField()
#     detail = StringField()
#     from_company = StringField()
#     성분등록번호 = StringField()
#     img = StringField()

def searchbytitle(title):
    foodlist = []
    findfood = db.food.find({'title':title}) #{'title':title}
    for f in findfood:
        foodlist.append(f)
    return foodlist
    # for food in Food.objects:
    #     return food

def searchbyid(index):
    foodlist = []
    findfood = db.food.find({'index':index})
    for f in findfood:
        foodlist.append(f)
    return foodlist