from random import randrange
from typing import Optional
import pydantic
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    description: str
    content: bool=False
    date: str="one"
    rating: Optional[int]=None

sample_posts=[{"title":"title1","description":"description1","content":"content1","date":"date1","rating":"rating1"},{"title":"title2","description":"description2","content":"content2","date":"date2","rating":"rating2"}]

@app.get("/")
def root():
    print()
    return {"message": "Helloooooo Worldddddddddddd"}



@app.get("/post")
def get_posts():
    print("get_post initiated")
    return {"message": sample_posts}



@app.post("/post")
def create_post(payload: Post):
    print(payload)
    print(payload.dict())
    payload_dict= payload.dict()
    payload_dict['id']=randrange(0,1000000)
    sample_posts.append(payload_dict)
    print(sample_posts)
    return {"data": f"returning id of new post created with unique_id: {payload_dict['id']} title: {payload_dict['title']} content: {payload_dict['content']}" }


