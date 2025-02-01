from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    database_password:str="localhost"
    database_username:str="postgres"
    secret_key:str="adnfla"

setting=Setting()