from typing import Optional, Union
from fastapi import  FastAPI,Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

list_of_posts = [{"title":"title1","content":"content1","id":1},{"title":"title2","content":"content2","id":2}]

class Post(BaseModel):
    title:str
    content:str
    id:Optional[int]=None

#fastapi works on the first match principle, meaning if a bunch of api has the same path, it'll pick the one that matched first
@app.get("/posts/helloWorld")
def read_root():
    return {"Hello": "World"}

@app.get("/posts/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/posts")
def firstapi():
    return {"message":list_of_posts}

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
    payload_dict=payload.model_dump()
    payload_dict["id"] = randrange(0,10000000)
    if not any(post["id"]==payload_dict["id"]  for post in list_of_posts):
        list_of_posts.append(payload_dict)
    else:
        return {
                "message":"cannot add post, Post id already exists",
                "list of posts": list_of_posts
                }
    return list_of_posts

def findPostById(id):
    post=next((post for post in list_of_posts if post["id"]==id),None)
    if post:
        return post
    else:
        return None

@app.get("/posts/{id}")
def getPostById(id:int,response:Response):
    post= findPostById(id)
    if post:
        return post
    else:
        response.status_code=404
        return {"message":"No post found for the given ID"}
    