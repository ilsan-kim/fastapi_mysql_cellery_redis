from typing import Any
import re
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.ext.declarative import declarative_base


@as_declarative()
class Base:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    __name__: str

    # CamelCase의 클래스 이름으로부터 snake_case의 테이블 네임 자동 생성
    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()


def same_as(column_name):
    def default_function(context):
        return context.current_parameters.get(column_name)
    return default_function


BaseNoDatetime = declarative_base(metadata=None)