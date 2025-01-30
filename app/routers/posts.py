from fastapi import  FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oath2
from ..schemas import Post,createUser
from sqlalchemy.exc import IntegrityError
from ..database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session
from typing import Optional, Union,List

router=APIRouter(prefix="/posts",
                 tags=['Posts'])


@router.get("/",response_model=List[schemas.ResponseBody])
def firstapi(db: Session = Depends(get_db), user_id:int = Depends(oath2.get_current_user)):
    posts=db.query(models.Post).filter(models.Post.id==user_id.id).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseBody)
def postBody(payload:Post,db: Session = Depends(get_db), user_id:int = Depends(oath2.get_current_user)):
    new_Post = models.Post( Owner_id=user_id.id,**payload.model_dump())
    #print(user_id.email)
    db.add(new_Post)
    db.commit()
    db.refresh(new_Post)
    return new_Post



@router.get("/{id}",response_model=schemas.ResponseBody)
def getPostById(id:int,db: Session = Depends(get_db), user_id:int = Depends(oath2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    return posts
    

@router.delete("/{id}",status_code=status.HTTP_202_ACCEPTED)
def deletePostById(id:int,db: Session = Depends(get_db), user_id:int = Depends(oath2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    post=posts.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    if post.Owner_id!=user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"id of {id} not authorised to perform requested action")
    posts.delete(synchronize_session=False)
    db.commit()
    return {"message":f"The Post with the id of {id} has been deleted"}



@router.put("/{id}",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseBody)
def updatePostById(id:int,post:Post,db: Session = Depends(get_db), user_id:int = Depends(oath2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    posts = post_query.first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    if posts.Owner_id!=user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"id of {id} not authorised to perform requested action")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return  {"message":"The following posts have been updated",
            "posts":post_query.first()}


