from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .db_info import adminster
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{name}:{password}@{server}/{database}".format(name=adminster.admin_name,password = adminster.admin_pass, server = adminster.admin_server,database = adminster.admin_db)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()