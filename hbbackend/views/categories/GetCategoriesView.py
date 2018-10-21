from sanic import response
from sanic.views import HTTPMethodView
from sanic.log import logger

import json

from hbbackend.users.model import find_user_by_email
from hbbackend.util.crypto import decrypt_data
from hbbackend.commons import default_categories


class GetCategoriesView(HTTPMethodView):

    async def post(self, request):
        json_request = request.json

        if 'email' not in json_request or 'password' not in json_request:
            return response.json({"error": {"message": "email/pass missing"}},
                                 status=422)

        user = await find_user_by_email(json_request['email'])

        if not user or 'preferences' not in user \
           or 'categories_encrypted' not in user['preferences']:
            return response.json({'error': {"message": 'no such user'}},
                                 status=422)

        data = decrypt_data(
            user['preferences']['categories_encrypted'],
            json_request['password']
        )
        categories = data['decrypted']

        logger.info(f"Decrypting categories took {data['time_ms']}ms")

        if categories is '':
            return response.json({'error': {"message": 'incorrect password'}},
                                 status=422)

        # NASTY HACK \o/
        if categories == '[]':
            categories_json = json.loads(
                json.dumps(default_categories)
                .replace("$NAME", user['lastName'])
            )
        else:
            categories_json = json.loads(categories)

        return response.json({
            'email': user['email'],
            'id': str(user['_id']),
            'categories': categories_json
        })
