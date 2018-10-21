"""
https://youtu.be/HHill_kR-FQ
"""

from sanic import Sanic

import os

from hbbackend.routes import setup_routes
from hbbackend.db import create_client
import hbbackend.commons

app = Sanic()


@app.listener('before_server_start')
def init(sanic, loop):
    client = create_client(io_loop=loop)
    hbbackend.commons.db = client['hyperbudget-dev']


if __name__ == "__main__":
    setup_routes(app)

    app.run(host=os.environ.get("HOST", "0.0.0.0"),
            port=os.environ.get("PORT", 8000))
