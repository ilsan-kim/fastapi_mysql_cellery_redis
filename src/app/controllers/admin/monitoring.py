"""
For Admin API : 검수
"""
from datetime import datetime, timedelta
from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.admin import monitoring
from app.controllers import deps

router = APIRouter()


@router.get("/statistic", response_model=monitoring.SeriesStatusStatistic)
def get_monitoring_statistic(
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get Series for Monitoring. API Server adjust UCT to KST by itself
    """
    series_list = crud.series_status.get_all(db=db)

    total = len(series_list)

    # 필터 함수를 위한 시간대 설정
    now_month = datetime.now().month
    this_month_end = (datetime.now() + timedelta(hours=9)).replace(month=now_month + 1, day=1, hour=0, minute=0, second=0)
    this_month_start = (datetime.now() + timedelta(hours=9)).replace(day=1, hour=0, minute=0, second=0)
    prev_month_start = (datetime.now() + timedelta(hours=9)).replace(month=now_month - 1, day=1, hour=0, minute=0, second=0)
    preprev_month_start = (datetime.now() + timedelta(hours=9)).replace(month=now_month - 2, day=1, hour=0, minute=0, second=0)

    # 등록건수 확인 > 이번달 시작일 ~ 이번달 종료일 사이에 생성된 시리즈 정보
    this_month_registered = list(
        filter(lambda series: this_month_start <= series.created_at + timedelta(hours=9) < this_month_end,
               [series for series in series_list]))

    # 처리건수 확인 > 이번달 시작일 ~ 이번달 종료일 사이에 상태 변경된 시리즈 정보
    this_month_processed = list(
        filter(lambda series:
               this_month_start <= series.updated_at + timedelta(hours=9) < this_month_end and series.status == "APPROVED",
               [series for series in series_list]))

    # 누적 미처리건 > 전체 미처리건 정보
    this_month_unprocessed = list(
        filter(lambda series: series.status == "UNAPPROVED",
               [series for series in series_list]))

    prev_month_registered = list(
        filter(lambda series: prev_month_start <= series.created_at + timedelta(hours=9) < this_month_start,
               [series for series in series_list]))

    prev_month_processed = list(
        filter(lambda series:
               prev_month_start <= series.updated_at + timedelta(hours=9) < this_month_start and series.status == "APPROVED",
               [series for series in series_list]))

    prev_month_unprocessed = list(
        filter(lambda series:
               series.updated_at + timedelta(hours=9) < this_month_start and series.status == "UNAPPROVED",
               [series for series in series_list]))

    preprev_month_registered = list(
        filter(lambda series: preprev_month_start <= series.created_at + timedelta(hours=9) < prev_month_start,
               [series for series in series_list]))

    preprev_month_processed = list(
        filter(lambda series:
               preprev_month_start <= series.updated_at + timedelta(hours=9) < prev_month_start and series.status == "APPROVED",
               [series for series in series_list]))

    preprev_month_unprocessed = list(
        filter(lambda series:
               series.updated_at + timedelta(hours=9) < prev_month_start and series.status == "UNAPPROVED",
               [series for series in series_list]))

    this_month = {
        "month": 1,
        "registered": len(this_month_registered),
        "processed": len(this_month_processed),
        "unprocessed": len(this_month_unprocessed)
    }
    prev_month = {
        "month": 2,
        "registered": len(prev_month_registered),
        "processed": len(prev_month_processed),
        "unprocessed": len(prev_month_unprocessed)
    }
    preprev_month = {
        "month": 3,
        "registered": len(preprev_month_registered),
        "processed": len(preprev_month_processed),
        "unprocessed": len(preprev_month_unprocessed)
    }
    return {"total": total, "detail": [this_month, prev_month, preprev_month]}


@router.get("/table")
def get_monitoring_table(
        *,
        db: Session = Depends(deps.get_db),
        page_request: dict = Depends(deps.get_page_request)
) -> Any:
    return crud.series_status.get_paginated(db=db, page_request=page_request)
