from fastapi import Depends,status,APIRouter,HTTPException,Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils
from .. import oath2

router=APIRouter(tags=['Authentication'])

@router.post('/login')
def login(usercred:schemas.userAuth,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.email==usercred.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')
    if not utils.verify(usercred.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')
    token=oath2.create_access_token(data={'email':usercred.email})
    return {"token":token}