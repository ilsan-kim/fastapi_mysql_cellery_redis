from typing import Any

from fastapi import APIRouter

from app.core.config import settings
from app.controllers.admin import (
    series,
    field,
    banned_string
)

api_router_admin = APIRouter()
api_router_admin.include_router(series.router, prefix='/series', tags=['admin/series'])
api_router_admin.include_router(field.router, prefix='/filed', tags=['admin/field'])
api_router_admin.include_router(banned_string.router, prefix='/banned_string', tags=['admin/banned_string'])
