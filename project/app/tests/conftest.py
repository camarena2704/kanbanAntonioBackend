import json

import pytest
from fastapi import FastAPI
from requests.models import Response
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.app_config import AppSettings, get_application_settings
from app.main import create_app
from app.modules.database_module.settings import module_settings


class TestAPP:

    def __init__(self, test_app, test_app_url):
        """
        Instance the test application
        """
        self.test_app = test_app
        self.test_app_url = test_app_url

        # Init empty variables
        self.tokens = {}

    def do_request(
        self, http_method: str, endpoint: str, headers: dict = None, data: dict = None
    ) -> Response:
        """
        Make a request to the app and return response
        :param http_method: http method (get/post/put/delete)
        :param endpoint: endpoint to call
        :param headers: headers of the request
        :param data: data of the request
        :return: response from the server
        :rtype: Response
        """

        return self.test_app.request(
            http_method,
            f"{self.test_app_url}{endpoint}",
            headers=headers if headers else None,
            data=json.dumps(data) if data else None,
        )

    def do_request_with_role(
        self,
        role: str,
        http_method: str,
        endpoint: str,
        headers: dict = None,
        data: dict = None,
    ) -> Response:
        """
        Make a request to the app with specific role and return response
        :param role: role to login and make the request
        :param http_method: http method (get/post/put/delete)
        :param endpoint: endpoint to call
        :param headers: headers of the request
        :param data: data of the request
        :return: response from the server
        :rtype: Response
        """

        # Get token from role
        token = self.get_token_for_role(role)

        return self.do_request(
            http_method,
            endpoint,
            headers={**{"Authorization": f"Bearer {token}"}, **(headers or {})},
            data=data,
        )


@pytest.fixture(scope="session")
def test_app() -> TestAPP:
    # Init app
    test_app: FastAPI = create_app()

    # Override the test application settings
    test_app_config = AppSettings()
    test_app.dependency_overrides[get_application_settings] = test_app_config

    # Init Tortoise for database
    register_tortoise(
        test_app,
        db_url=module_settings.database_url,
        modules={"default": ["app.modules.database_module.models.default"]},
    )

    with TestClient(test_app) as test_client:
        yield TestAPP(test_client, f"/api/v{test_app_config.api_version}")


def pytest_collection_modifyitems(items):
    order = {
        "primer_tests.py": 0,
    }

    def sort_key(item):
        filename = item.nodeid.split("::")[0].replace("\\", "/")
        shortname = filename.split("integration/")[-1]
        return order.get(shortname, 999)

    items.sort(key=sort_key)
