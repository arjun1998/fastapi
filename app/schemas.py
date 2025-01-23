from pydantic import BaseModel,EmailStr
from typing import Optional, Union, List
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published:Optional[bool]=False
    #id:Optional[int]=None

class Post(PostBase):
    pass

class userAuth(BaseModel):
    email:EmailStr
    password:str

class ResponseBody(BaseModel):
    id:int
    title:str
    content:str
    created_at:datetime

    class Config:
        orm_mode = True

class createUser(BaseModel):
    email:EmailStr
    password:str

    class Config:
        orm_mode = True


class createUserResponseBody(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime



    class Config:
        orm_mode = True


