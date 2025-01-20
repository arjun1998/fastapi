from typing import Optional, Union,List
from fastapi import  FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.exc import IntegrityError
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import time
from . import models
from .schemas import Post,createUser
from . import schemas
from . import utils
from .database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session





app = FastAPI()

models.Base.metadata.create_all(bind=engine)



@app.get("/posts",response_model=List[schemas.ResponseBody])
def firstapi(db: Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseBody)
def postBody(payload:Post,db: Session = Depends(get_db)):
    new_Post = models.Post(**payload.model_dump())
    db.add(new_Post)
    db.commit()
    db.refresh(new_Post)
    return new_Post



@app.get("/posts/{id}",response_model=schemas.ResponseBody)
def getPostById(id:int,db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    return posts
    

@app.delete("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def deletePostById(id:int,db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    post=posts.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    
    posts.delete(synchronize_session=False)
    db.commit()
    return {"message":f"The Post with the id of {id} has been deleted"}



@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseBody)
def updatePostById(id:int,post:Post,db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return  {"message":"The following posts have been updated",
            "posts":post_query.first()}


@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.createUserResponseBody)
def createUsers(user:createUser,db: Session = Depends(get_db)):
    hashed_pwd=utils.hash(user.password)
    user.password=hashed_pwd

    new_Post = models.Users(**user.model_dump())
    try:
        db.add(new_Post)
        db.commit()
        db.refresh(new_Post)
        return new_Post
    except IntegrityError as e:
        db.rollback()
        # Custom error message handling for duplicate keys
        if 'duplicate key value violates unique constraint' in str(e.orig):
            raise HTTPException(status_code=400, detail=f"User with email {user.email} already exists.")
        raise HTTPException(status_code=400, detail="Failed to create user due to a constraint violation.")

    except Exception as e:
        db.rollback()
        # General error handling
        raise HTTPException(status_code=500, detail=str(e))
    


    
    

@app.delete("/users/{id}",status_code=status.HTTP_202_ACCEPTED)
def deleteUserById(id:int,db: Session = Depends(get_db)):
    posts = db.query(models.Users).filter(models.Users.id == id)
    post=posts.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id of {id} not found")
    
    posts.delete(synchronize_session=False)
    db.commit()
    return {"message":f"The User with the id of {id} has been deleted"}


@app.get("/users/{id}",status_code=status.HTTP_200_OK,response_model=schemas.createUserResponseBody)
def getUserByID(id:int,db: Session = Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not found")
    return user