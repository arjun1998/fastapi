import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta

SECRET_KEY = "331026042656cf0dbadbd15eb7bb461a32b3aeb7a899f4e884b8a549e2657c0e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    encode_data=data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_data.update({'exp':expire})
    token=jwt.encode(encode_data,SECRET_KEY,algorithm=ALGORITHM)
    return token