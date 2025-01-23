from fastapi import Depends,status,APIRouter,HTTPException,Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils

router=APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials:schemas.UserLogin,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.email==user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')