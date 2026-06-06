"""
Routing smoke tests — verifies OPTIONS preflight routes are reachable
(regression for the double-slash blueprint prefix bug fixed in Sanic 24+).
"""
import pytest
from sanic import Sanic, response
from sanic_testing import TestManager

from hbbackend.api.v1 import api_v1


@pytest.fixture
def app():
    # Use a unique name per test run to avoid Sanic's app-registry collisions
    test_app = Sanic("test_routing")
    TestManager(test_app)

    test_app.blueprint(api_v1)

    @test_app.middleware("response")
    async def cors(request, resp):
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Headers"] = "*"

    return test_app


OPTIONS_ROUTES = [
    "/account/login",
    "/account/register",
    "/account/reset-password",
    "/account/confirm-reset-password",
    "/account/categories/list",
    "/account/categories/update",
    "/account/transactions/list",
    "/account/transactions/update",
]


@pytest.mark.parametrize("path", OPTIONS_ROUTES)
def test_options_returns_200(app, path):
    _, resp = app.test_client.options(path)
    assert resp.status == 200, f"OPTIONS {path} returned {resp.status}, expected 200"


@pytest.mark.parametrize("path", OPTIONS_ROUTES)
def test_options_cors_headers(app, path):
    _, resp = app.test_client.options(path)
    assert "Access-Control-Allow-Origin" in resp.headers
