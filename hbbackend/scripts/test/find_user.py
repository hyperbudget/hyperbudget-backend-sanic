import asyncio
from pprint import pprint

from hbbackend.db import create_client
from hbbackend.users.model import find_user_by_email


async def get_user(email):
    client = create_client()
    user = await find_user_by_email(client['hyperbudget-dev'], email)
    pprint(user['email'] + " " + str(user['_id']))


asyncio.get_event_loop().run_until_complete(get_user('errietta@errietta.me'))
asyncio.get_event_loop().run_until_complete(get_user('errietta2@errietta.me'))
