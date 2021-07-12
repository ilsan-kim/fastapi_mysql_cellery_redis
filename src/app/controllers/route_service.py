from typing import Any

from fastapi import APIRouter

from app.controllers.v1 import (
    user,
    writer,
    novel,
    series
)

api_router_service = APIRouter()
api_router_service.include_router(user.router, prefix='/user', tags=['user'])
api_router_service.include_router(writer.router, prefix='/writer', tags=['writer'])
api_router_service.include_router(novel.router, prefix='/novel', tags=['novel'])


@api_router_service.get('/')
def health_check() -> Any:
    return {}