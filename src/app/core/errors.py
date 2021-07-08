from fastapi import HTTPException


class NovelException(Exception):
    def __init__(self, msg, *args):
        self._error_message = f'{msg} in {args}'

    def __str__(self):
        return self._error_message
