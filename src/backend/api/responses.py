from http import HTTPStatus
from typing import Any


def create_error_responses(
    error_responses: dict[int, dict[str, dict[str, Any]]]
) -> dict:
    responses = {}

    for status_code, examples in error_responses.items():
        description = HTTPStatus(status_code).phrase
        responses[status_code] = {
            "description": description,
            "content": {"application/json": {"examples": examples}},
        }

    return responses


get_top_100_repo_exceptions = {
    400: {
        "format_error": {
            "summary": "FormatIsIncorrect",
            "value": {
                "detail": "The format to sort params is incorrect. The correct format is 'param1, param2, etc'"
            },
        },
        "param_error": {
            "summary": "ParamIsIncorrect",
            "value": {"detail": "The sort param is not valid"},
        },
    },
    500: {
        "interanal_server_error": {
            "summary": "RuntimeError",
            "value": {"detail": "A runtime error occurred"},
        }
    },
}

get_repo_activity_exceptions = {
    400: {
        "incorrect_date_format": {
            "summary": "DateFormatIsIncorrect",
            "value": {"detail": "The date format must be YYYY-MM-dd"},
        },
    },
    404: {
        "owner_not_found": {
            "summary": "OwnerDoesNotExist",
            "value": {"detail": "Inserted owner was not found"},
        },
        "repo_not_found": {
            "summary": "RepoDoesNotExist",
            "value": {"detail": "Inserted repo was not found"},
        },
    },
    409: {
        "until_is_biger_than_since": {
            "summary": "UntilIsBiggerThanSince",
            "value": {"detail": "Until could not be bigger than since"},
        },
    },
    500: {
        "interanal_server_error": {
            "summary": "RuntimeError",
            "value": {"detail": "A runtime error occurred"},
        }
    },
}


get_top_100_repo_responses = create_error_responses(get_top_100_repo_exceptions)
get_repo_activity_responses = create_error_responses(get_repo_activity_exceptions)
