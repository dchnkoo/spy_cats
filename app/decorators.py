from fastapi import HTTPException, status
from functools import wraps

import typing as _t


def error_handler(func: _t.Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AssertionError as e:
            status_code, msg = str(e).split(":")
            raise HTTPException(int(status_code), detail=msg.strip())
        except Exception as e:
            print(e)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper
