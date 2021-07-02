import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)