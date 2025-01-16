from pydantic import BaseModel
from typing import Optional, Union

class Post(BaseModel):
    title:str
    content:str
    published:Optional[bool]=False
    #id:Optional[int]=None