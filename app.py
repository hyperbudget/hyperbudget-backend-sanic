"""
https://youtu.be/HHill_kR-FQ
"""

import aiohttp
from dotenv import load_dotenv

from sanic import Sanic, response
from sanic_cors import CORS

import os
import re

from pymongo.errors import ServerSelectionTimeoutError

from hbbackend.views.account.LoginView import LoginView
from hbbackend.views.account.RegisterView import RegisterView

from hbbackend.views.transactions.UpdateTransactionsView import \
    UpdateTransactionsView
from hbbackend.views.transactions.GetTransactionsView import \
    GetTransactionsView
from hbbackend.views.categories.GetCategoriesView import GetCategoriesView
from hbbackend.views.categories.UpdateCategoriesView import \
    UpdateCategoriesView

from hbbackend.views.account.PwdResetView import PwdResetView
from hbbackend.views.account.DoResetView import DoResetView

from hbbackend.db import create_client
import hbbackend.commons

load_dotenv()
app = Sanic()


@app.listener('before_server_start')
async def init(sanic, loop):
    await setup_mongo(loop)
    await setup_aiohttp(loop)


@app.listener('before_server_stop')
async def stop(sanic, loop):
    await hbbackend.commons.aiohttp.close()


async def setup_aiohttp(loop):
    hbbackend.commons.aiohttp = aiohttp.ClientSession(loop=loop)


async def setup_mongo(loop):
    host = os.environ.get('MONGODB_URI',
                          'mongodb://localhost:27017/hyperbudget-dev')
    client = create_client(
        io_loop=loop,
        host=host
    )

    match = re.match(r'^mongodb://\S+/(\S+)$', host)

    if not match:
        print("couldn't get db name")
        exit(1)

    hbbackend.commons.db = client[match.group(1)]

    try:
        await client.admin.command('ismaster')
    except ServerSelectionTimeoutError:
        print("Could not connect to db")
        exit(1)


@app.route('/')
def index(request):
    return response.json({
        "ok": True,
        "version": hbbackend.__version__
    })


def setup_commons():
    hbbackend.commons.services = {
        key: os.environ[key] for key in [
            'PWD_RESET_SERVICE'
        ]
    }
    hbbackend.commons.api_keys = {
        key: os.environ[key] for key in [
            'PWD_RESET_SERVICE_KEY'
        ]
    }


if __name__ == "__main__":
    setup_commons()

    CORS(app, automatic_options=True)
    app.add_route(LoginView.as_view(), '/account/login')
    app.add_route(RegisterView.as_view(), '/account/register')
    app.add_route(GetTransactionsView.as_view(), '/account/transactions/list')
    app.add_route(UpdateTransactionsView.as_view(),
                  '/account/transactions/update')
    app.add_route(GetCategoriesView.as_view(), '/account/categories/list')
    app.add_route(UpdateCategoriesView.as_view(),
                  '/account/categories/update')

    app.add_route(PwdResetView.as_view(), '/account/reset-password')
    app.add_route(DoResetView.as_view(), '/account/confirm-reset-password')

    app.run(host=os.environ.get("HOST", "0.0.0.0"),
            port=os.environ.get("PORT", os.environ.get('PORT', 8000)),
            access_log=True)
