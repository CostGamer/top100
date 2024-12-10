from typing import AsyncGenerator
from unittest.mock import MagicMock

import pytest
from httpx import ASGITransport, AsyncClient
from pytest_mock import MockerFixture
from requests.models import Response

from src.backend.main import setup_app
from tests.fake_items import fake_data


@pytest.fixture
def mock_github_api(mocker: MockerFixture) -> Response:
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = fake_data
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response


@pytest.fixture
def mock_db_data() -> list:
    return fake_data["items"]


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    app = setup_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
