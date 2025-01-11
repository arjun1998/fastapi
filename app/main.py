from typing import Optional, Union
from fastapi import  FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import time



load_dotenv()
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
#DB connection setup
while True:
    try:  
        conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        cursor_factory=RealDictCursor
    )
        cur = conn.cursor()
        print("Connected to the database!")
        break
    except Exception as error:
        print("Connection failed, Error",error)
        time.sleep(2)





app = FastAPI()

list_of_posts = [{"title":"title1","content":"content1","id":1},{"title":"title2","content":"content2","id":2}]


class Post(BaseModel):
    title:str
    content:str
    published:Optional[bool]=False
    id:Optional[int]=None

def findPostById(id):
    post=next((post for post in list_of_posts if post["id"]==id),None)
    if post:
        return post
    else:
        return None
def findIndexById(id):
    for index,post in enumerate(list_of_posts):
        if post["id"]==id:
            return index


#fastapi works on the first match principle, meaning if a bunch of api has the same path, it'll pick the one that matched first
@app.get("/posts/helloWorld")
def read_root():
    return {"Hello": "World"}

@app.get("/posts/items/{item_id}")
def read_item(item_id: int):
    cur.execute(""" Select * from posts where id = %s  """,item_id)
    posts=cur.fetchall()
    return {"post": posts}

@app.get("/posts")
def firstapi():
    cur.execute(""" Select * from posts  """)
    posts=cur.fetchall()
    conn.commit()
    return {"posts":posts}

@app.post("/posts/postId/{postId}")
def firstPost(postId:int,q:Union[int,None]=None):
    return {"postId":postId,"q":q}

@app.post("/posts/Body")
def postBody(payload:dict = Body(...)):
    print(payload)
    return{"payload":payload
           ,"welcome":"to the top"}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def postBody(payload:Post):
    cur.execute("""Insert into posts (title,content,published) values (%s,%s,%s) RETURNING *""",(payload.title,payload.content,payload.published))
    new_post = cur.fetchone()
    return {"post":new_post}



@app.get("/posts/{id}")
def getPostById(id:int):
    cur.execute(""" Select * from posts where id = %s  """,(id,))
    posts=cur.fetchone()
    conn.commit()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    return {"post": posts}
    

@app.delete("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def deletePostById(id:int):
    cur.execute("""  Delete from posts where id = %s returning * """,(id,))
    posts=cur.fetchone()
    conn.commit()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
    return {"message":"The following posts have been deleted",
            "posts":posts}



@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def updatePostById(id:int,post:Post):
    cur.execute("""  UPDATE posts set title = %s,content=%s,published=%s where id = %s returning * """,(post.title,post.content,post.published,id,))
    posts=cur.fetchone()
    conn.commit()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id of {id} not found")
   
    return  {"message":"The following posts have been updated",
            "posts":posts}


# conn.commit()
# cur.close()
# conn.close()