from typing import Optional, List, Dict

from pydantic import BaseModel


'''
basic series status statistic schema class for API response
'''


# Shared properties
class MonthlyData(BaseModel):
    month: int
    registered: int
    processed: int
    unprocessed: int


# Properties of API Response
class SeriesStatusStatistic(BaseModel):
    total: int
    detail: List[MonthlyData]

    class Config:
        orm_mode = True
