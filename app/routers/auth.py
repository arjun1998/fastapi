from fastapi import Depends,status,APIRouter,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils
from .. import oath2

router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.token)
def login(usercred:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.email==usercred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    if not utils.verify(usercred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Invalid Credentials')
    token=oath2.create_access_token(data={'id':user.id})
    return {"access_token":token,'token_type':'bearer'}