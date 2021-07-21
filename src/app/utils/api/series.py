from typing import Any

from fastapi.encoders import jsonable_encoder

def get_meta_from_meta_list(meta_list: list, comparison: str, criteria: Any, value: str):
    """
    메타데이터 리스트에서 원하는 대조군과 그 결과값을 기반으로 메타데이터 dict에서 특정 key의 value를 꺼내옵니다.\n
    :param meta_list: 작품이나 회차의 메타정보 리스트 (series.series_meta 혹은 novel.novel_meta)\n
    :param comparison:  비교군 ("is_origin" 혹은 'language_code")\n
    :param criteria:  비교값 (is_origin > bool로 비교 // language_code > string으로 비교)\n
    :param value:  꺼내올 값 (title, description 등)\n
    :return: 꺼내온 값
    """
    if comparison == "is_origin" or comparison == "language_code":
        return list(filter(lambda x: x.get(comparison) == criteria, [meta for meta in jsonable_encoder(meta_list)]))[0].get(value)
    raise NameError
