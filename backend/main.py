from random import randrange
from re import S
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

sample_posts=[{"id": 1,"title":"title1","description":"description1","content":"content1","date":"date1","rating":"rating1"},{"id":2,"title":"title2","description":"description2","content":"content2","date":"date2","rating":"rating2"}]

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


def find_post(id):
    for posti in sample_posts:
        if posti["id"]==id:
            return posti


# the order of the api routes specified in this file matters 
# as based on that the priority of the posts is decided 
# and the first route that matches the incoming request processes it 
@app.get("/post/test-pass-1234")
def get_latest_post():
    postl=sample_posts[len(sample_posts)-1]
    return {"detail": postl}


@app.get("/post/{id}")
def get_post(id: int):
    print(type(id))
    print(id)
    posta=find_post(id)
    print(posta)
    return {"post_data": f"the post id is {id} , and the post is {posta} "}

@app.get("/post/test-fail-1234")
def get_latest_post():
    postl=sample_posts[len(sample_posts)-1]
    return {"detail": postl}


