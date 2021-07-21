from typing import List

from fastapi.encoders import jsonable_encoder
from app.schemas.series import Series


def get_sum_of_count(series: List[Series], category: str):
    if series:
        try:
            series_statistic_list = list(filter(lambda x: x is not None, [s.series_statistic for s in series]))
            count = sum([jsonable_encoder(series_statistic).get(category) for series_statistic in series_statistic_list])
            return count
        except:
            return 0
    else:
        return 0


def get_avg_rating(series: List[Series]):
    try:
        return round(get_sum_of_count(series=series, category="rating")/len(series), 1)
    except ZeroDivisionError:
        return 0
