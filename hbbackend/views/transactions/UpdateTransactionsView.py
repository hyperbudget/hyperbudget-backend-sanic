from sanic import response
from sanic.views import HTTPMethodView
from sanic.log import logger

import json

from hbbackend.users.model import find_user_by_email, update_user
from hbbackend.util.crypto import decrypt_data, encrypt_data


class UpdateTransactionsView(HTTPMethodView):

    async def post(self, request):
        json_request = request.json

        if 'email' not in json_request or 'password' not in json_request \
           or 'transactions' not in json_request:
            return response.json({"error": {"message": "data missing"}},
                                 status=422)

        user = await find_user_by_email(json_request['email'])

        if not user or 'settings' not in user:
            return response.json({'error': {'message': 'no such user'}},
                                 status=422)

        data = decrypt_data(
            user['settings'],
            json_request['password']
        )
        settings = data['decrypted']

        logger.info(f'Decrypting settings took {data["time_ms"]}ms')

        if settings is '':
            return response.json({'error': {'message': 'incorrect password'}},
                                 status=422)

        data = encrypt_data(
            json.dumps(json_request['transactions']),
            json_request['password']
        )

        logger.info(f'Encrypting transactions took {data["time_ms"]}ms')

        await update_user(
            json_request['email'],
            {
                'data': {
                    'transactions_encrypted': data['encrypted_b64']
                }
            }
        )

        return response.json({
            'ok': True
        })
