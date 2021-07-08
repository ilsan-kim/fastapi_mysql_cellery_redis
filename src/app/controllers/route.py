from typing import Any

from fastapi import APIRouter

from app.controllers.v1 import (
    user,
    field,
    writer,
    novel,
    banned_string
)


api_router = APIRouter()
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(field.router, prefix='/filed', tags=['field'])
api_router.include_router(writer.router, prefix='/writer', tags=['writer'])
api_router.include_router(novel.router, prefix='/novel', tags=['novel'])
api_router.include_router(banned_string.router, prefix='/banned_string', tags=['banned_string'])


@api_router.get('/')
def health_check() -> Any:
    return {}