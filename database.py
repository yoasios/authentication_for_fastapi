from sqlalchemy import create_engine , Column , Integer , String
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, echo=True)
localsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

def get_db():
    db = localsession()
    try:
        yield db
    finally:
        db.close()