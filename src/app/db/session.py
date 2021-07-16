import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

database_uri = f"mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_SERVER}:3306/{settings.MYSQL_DB}?charset=utf8mb4"
engine = create_engine(database_uri, pool_pre_ping=True, pool_size=15, max_overflow=0, encoding='utf8', convert_unicode=True)
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)