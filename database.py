from sqlalchemy import create_engine , Column , Integer , String
from sqlalchemy.orm import sessionmaker , declarative_base

engine = create_engine("sqlite:///./test.db", echo=True)
localsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

def get_db():
    db = localsession()
    try:
        yield db
    finally:
        db.close()