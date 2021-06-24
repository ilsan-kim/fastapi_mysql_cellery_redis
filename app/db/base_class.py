from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __table__name__ automatically
    @declared_attr
    def __table__name(cls) -> str:
        return cls.__name__.lower()