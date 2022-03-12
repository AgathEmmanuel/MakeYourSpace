from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Helloooooo Worldddddddddddd"}


@app.get("/posts")
def get_posts():
    return {"data": "display you posts "}


@app.get("/createpost")
def create_post(payload: dict=Body(...)):
    print(payload)
    return {"message": "created new pos successffully"}


