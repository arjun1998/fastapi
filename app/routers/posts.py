from fastapi import  FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from ..schemas import Post,createUser
from sqlalchemy.exc import IntegrityError
from ..database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import Optional, Union,List

router=APIRouter()


@router.get("/posts",response_model=List[schemas.ResponseBody])
def firstapi(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts


@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseBody)
def postBody(payload:Post,db: Session = Depends(get_db)):
    new_Post = models.Post(**payload.model_dump())
    db.add(new_Post)
    db.commit()
    db.refresh(new_Post)
    return new_Post



@router.get("/posts/{id}",response_model=schemas.ResponseBody)
def getPostById(id:int,db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    return posts
    

@router.delete("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def deletePostById(id:int,db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    post=posts.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    
    posts.delete(synchronize_session=False)
    db.commit()
    return {"message":f"The Post with the id of {id} has been deleted"}



@router.put("/posts/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseBody)
def updatePostById(id:int,post:Post,db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return  {"message":"The following posts have been updated",
            "posts":post_query.first()}

