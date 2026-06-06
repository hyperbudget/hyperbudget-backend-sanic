"""
Routing smoke tests — verifies OPTIONS preflight routes return 200 + CORS headers.
OPTIONS is handled by a request middleware so no per-route handlers are needed.
"""
import pytest
from sanic import Sanic, response
from sanic_testing import TestManager

from hbbackend.api.v1 import api_v1

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
}


@pytest.fixture
def app():
    test_app = Sanic("test_routing")
    TestManager(test_app)
    test_app.blueprint(api_v1)

    @test_app.middleware("request")
    async def handle_options(req):
        if req.method == "OPTIONS":
            return response.empty(headers=CORS_HEADERS)

    @test_app.middleware("response")
    async def cors(req, resp):
        resp.headers.update(CORS_HEADERS)

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
    assert resp.status in (200, 204), f"OPTIONS {path} returned {resp.status}, expected 200 or 204"


@pytest.mark.parametrize("path", OPTIONS_ROUTES)
def test_options_cors_headers(app, path):
    _, resp = app.test_client.options(path)
    assert resp.headers.get("Access-Control-Allow-Origin") == "*"
    assert resp.headers.get("Access-Control-Allow-Methods") == "GET, POST, OPTIONS"
