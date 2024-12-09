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

owner_does_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Inserted owner was not found",
)

repo_does_not_exist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Inserted repo was not found",
)

until_is_bigger_than_since = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Until could not be bigger than since",
)

incorrect_date_format = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The date format must be YYYY-MM-dd",
)
