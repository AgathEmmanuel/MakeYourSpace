from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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



# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

@app.get("/post")
def get_posts():
    print("get_post initiated")
    return {"message": sample_posts}



@app.post("/post",status_code=status.HTTP_201_CREATED)
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
def get_post(id: int, response: Response ):
    print(type(id))
    print(id)
    posta=find_post(id)
    print(posta)
    if not posta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
#        response.status_code= status.HTTP_404_NOT_FOUND
#        return {'message': f"post with id {id} was not found"}
    return {"post_data": f"the post id is {id} , and the post is {posta} "}

@app.get("/post/test-fail-1234")
def get_latest_post():
    postl=sample_posts[len(sample_posts)-1]
    return {"detail": postl}


def delete_post_index(id):
    for i,p in enumerate(sample_posts):
        if p['id']==id:
            print(p)
            return i

@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index=delete_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    sample_posts.pop(index)
    #return {'message': f"post with id {id} was deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


