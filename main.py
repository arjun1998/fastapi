from typing import Optional, Union
from fastapi import  FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    author: Optional[str]=None

#fastapi works on the first match principle, meaning if a bunch of api has the same path, it'll pick the one that matched first
@app.get("/posts/helloWorld")
def read_root():
    return {"Hello": "World"}

@app.get("/posts/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/posts")
def firstapi():
    return {"message":"Comfy learning"}

@app.post("/posts/postId/{postId}")
def firstPost(postId:int,q:Union[int,None]=None):
    return {"postId":postId,"q":q}

@app.post("/posts/Body")
def postBody(payload:dict = Body(...)):
    print(payload)
    return{"payload":payload
           ,"welcome":"to the top"}

@app.post("/posts")
def postBody(payload:Post):
    print(payload)
    return{"title":payload.title    ,
            "content":payload.content,
            "published":payload.published,
            "author":payload.author,
           "welcome":"to the top",
           "payload as an  pydantic object":payload,
           "payload as dictionary":payload.model_dump()
           }