"""
https://youtu.be/HHill_kR-FQ
"""

import os
import re

from dotenv import load_dotenv
from sanic import Sanic, response
from pymongo.errors import ServerSelectionTimeoutError

from hbbackend.api.v1 import api_v1
from hbbackend.db import create_client
import hbbackend.commons

load_dotenv()
app = Sanic(name='hperbudget-backend')

app.blueprint(api_v1)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
}


@app.middleware('request')
async def handle_options(req):
    if req.method == 'OPTIONS':
        return response.empty(headers=CORS_HEADERS)


@app.middleware('response')
async def cors(req, resp):
    resp.headers.update(CORS_HEADERS)


@app.listener('before_server_start')
async def init(sanic, loop):
    hbbackend.commons.services = {
        key: os.environ[key] for key in ['PWD_RESET_SERVICE']
    }
    hbbackend.commons.api_keys = {
        key: os.environ[key] for key in ['PWD_RESET_SERVICE_KEY']
    }
    await setup_mongo(loop)


async def setup_mongo(loop):
    host = os.environ.get('MONGODB_URI',
                          'mongodb://localhost:27017/hyperbudget-dev')
    client = create_client(
        io_loop=loop,
        host=host,
    )

    match = re.match(r'^mongodb://\S+/(\S+)$', host)

    if not match:
        match = re.match(r'^mongodb\+srv://\S+/(\S+)$', host)

    print(host)
    print(match)

    if not match:
        print("couldn't get db name")
        exit(1)

    hbbackend.commons.db = client[match.group(1)]

    try:
        await client.admin.command('ismaster')
    except ServerSelectionTimeoutError:
        print("Could not connect to db")
        exit(1)


@app.route('/', methods=['GET', 'OPTIONS'])
def index(request):
    return response.json({
        "ok": True,
        "version": hbbackend.__version__
    })


if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", 8000)),
            access_log=True)
