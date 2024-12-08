from fastapi import HTTPException, status


def with_errors(*error_exceptions: HTTPException) -> dict | None:
    """
    Collect all potential HTTP exceptions and format them for representation in an OpenAPI endpoint
    """
    if not error_exceptions:
        return None

    error_config = {}
    for error_num, exc in enumerate(error_exceptions, start=1):
        error_key = f"{exc.status_code}_{error_num}"

        error_config[error_key] = {
            "description": exc.detail or exc.__doc__ or "An error occurred"
        }

    return error_config


some_troubles_with_connection = HTTPException(
    status_code=status.HTTP_408_REQUEST_TIMEOUT,
    detail="Problems with query or connection",
)

params_incorrect_format = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The format to sort params is incorrect. The correct format is 'param1, param2, etc'",
)

param_not_valid = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The sort param is not valid",
)
