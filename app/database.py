from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()  # This is the new line to load .env file

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database_name = os.getenv("DB_NAME")

#SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}/{database_name}"

#SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s" % (username, password, host, database_name)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Arjun123@localhost/fastapi"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()