from fastapi import Request
from fastapi.responses import JSONResponse

from src.backend.app.interactions.custom_exceptions import (
    DateFormatIsIncorrect,
    FormatIsIncorrect,
    OwnerDoesNotExist,
    ParamIsIncorrect,
    RepoDoesNotExist,
    UntilIsBiggerThanSince,
)


async def params_incorrect_format(
    request: Request, exc: FormatIsIncorrect
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "detail": "The format to sort params is incorrect. The correct format is 'param1, param2, etc'"
        },
    )


async def param_not_valid(request: Request, exc: ParamIsIncorrect) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": "The sort param is not valid"},
    )


async def owner_does_not_exist(
    request: Request, exc: OwnerDoesNotExist
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Inserted owner was not found"},
    )


async def repo_does_not_exist(request: Request, exc: RepoDoesNotExist) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Inserted repo was not found"},
    )


async def until_is_bigger_than_since(
    request: Request, exc: UntilIsBiggerThanSince
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "Until could not be bigger than since"},
    )


async def incorrect_date_format(
    request: Request, exc: DateFormatIsIncorrect
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": "The date format must be YYYY-MM-dd"},
    )


async def runtime_error_exception_handler(
    request: Request, exc: RuntimeError
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "A runtime error occurred"},
    )
