import schemas
import models
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import engine, get_db

from typing import List


router = APIRouter(
    prefix="/post",
    tags=['Post']
)


# for this get request having .router() function we are getting a list as output
# and adding response_model=schemas.PostGetResponse results in validation error
@router.get("/",response_model=List[schemas.PostGetResponse])
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    print(type(posts))
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostCreateResponse)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post_new=models.Post(**payload.dict())
    db.add(post_new)
    db.commit()
    db.refresh(post_new)
    return post_new


@router.get("/{id}",response_model=schemas.PostGetResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post_with_id=db.query(models.Post).filter(models.Post.post_id==id).first()
    if not post_with_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post_with_id 


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_deleted=db.query(models.Post).filter(models.Post.post_id==id)
    if post_deleted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post_deleted.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.PostUpdateResponse)
def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db)):
    updated_payload = db.query(models.Post).filter(models.Post.post_id == id)
    if updated_payload.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    updated_payload.update(post.dict(),synchronize_session=False)
    db.commit()
    return post
