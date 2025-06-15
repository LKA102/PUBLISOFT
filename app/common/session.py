# Here we define the database session dependency for FastAPI.
# As all our modules will use SQLAlchemy, we will create a session dependency that can be used across the application.
# Note: But this does not mean that we will use SQLAlchemy in all modules. Each module can choose its own ORM or database library.

from config.settings import settings
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, declarative_base

database_url = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PWD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()