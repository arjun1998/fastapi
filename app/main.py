from typing import Optional, Union,List
from fastapi import  FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.exc import IntegrityError
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import time
from . import models
from .schemas import Post,createUser
from . import schemas
from . import utils
from .database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import posts,users,auth




app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)



    