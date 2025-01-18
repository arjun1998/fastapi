from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published:Optional[bool]=False
    #id:Optional[int]=None

class Post(PostBase):
    pass

class ResponseBody(BaseModel):
    id:int
    title:str
    content:str
    created_at:datetime

    class Config:
        orm_mode = True