from jose import jwt,JWTError
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta
from . import schemas
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

oath2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "331026042656cf0dbadbd15eb7bb461a32b3aeb7a899f4e884b8a549e2657c0e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    encode_data=data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_data.update({'exp':expire})
    token=jwt.encode(encode_data,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_access_token(token:str,credentials_exception):
    try:    
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        userid:str = payload.get('id')
        if userid is None:
            raise credentials_exception
        token_data = schemas.tokenData(id=userid)
    except JWTError:
        raise credentials_exception
    
def get_current_user(token:str =  Depends(oath2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate credentials',
                                          headers={"WWW-Authenticate":"Bearer"})
    
    return verify_access_token(token,credentials_exception)