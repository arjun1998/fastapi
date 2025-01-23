from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_pwd,hashed_pwd):
    return pwd_context.verify(plain_pwd,hashed_pwd)