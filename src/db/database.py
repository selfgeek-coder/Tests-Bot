from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from config import Config_obj

engine = create_engine(Config_obj.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)
