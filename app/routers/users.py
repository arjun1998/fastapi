from fastapi import  FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from ..schemas import Post,createUser
from sqlalchemy.exc import IntegrityError
from ..database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session

router=APIRouter()

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.createUserResponseBody)
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
    


    
    

@router.delete("/users/{id}",status_code=status.HTTP_202_ACCEPTED)
def deleteUserById(id:int,db: Session = Depends(get_db)):
    posts = db.query(models.Users).filter(models.Users.id == id)
    post=posts.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id of {id} not found")
    
    posts.delete(synchronize_session=False)
    db.commit()
    return {"message":f"The User with the id of {id} has been deleted"}


@router.get("/users/{id}",status_code=status.HTTP_200_OK,response_model=schemas.createUserResponseBody)
def getUserByID(id:int,db: Session = Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not found")
    return user