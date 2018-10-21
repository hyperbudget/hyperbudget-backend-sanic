"""
https://youtu.be/HHill_kR-FQ
"""

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

from hbbackend.db import create_client
import hbbackend.commons

app = Sanic()


@app.listener('before_server_start')
async def init(sanic, loop):
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


if __name__ == "__main__":
    CORS(app, automatic_options=True)
    app.add_route(LoginView.as_view(), '/account/login')
    app.add_route(RegisterView.as_view(), '/account/register')
    app.add_route(GetTransactionsView.as_view(), '/account/transactions/list')
    app.add_route(UpdateTransactionsView.as_view(),
                  '/account/transactions/update')
    app.add_route(GetCategoriesView.as_view(), '/account/categories/list')
    app.add_route(UpdateCategoriesView.as_view(),
                  '/account/categories/update')

    app.run(host=os.environ.get("HOST", "0.0.0.0"),
            port=os.environ.get("PORT", os.environ.get('PORT', 8000)),
            access_log=True)
