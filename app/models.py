from sqlalchemy.orm import Relationship
from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression  import text

class Post(Base):
    __tablename__= "posts"
    id = Column(Integer,primary_key= True, nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default=text('True'),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)
    Owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    Owner = Relationship("Users")


class Users(Base):
    __tablename__="users"
    id = Column(Integer,primary_key= True, nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)