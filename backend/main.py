import pydantic
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str


@app.get("/")
def root():
    return {"message": "Helloooooo Worldddddddddddd"}


@app.get("/posts")
def get_posts():
    return {"data": "display you posts "}


@app.get("/createpost")
def create_post(payload: dict=Body(...)):
    print(payload)
    return {"new_post": f"returning title {payload['title']} content: {payload['content']}"}


