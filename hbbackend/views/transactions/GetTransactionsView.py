from sanic import response
from sanic.views import HTTPMethodView
from sanic.log import logger

import json

from hbbackend.users.model import find_user_by_email
from hbbackend.util.crypto import decrypt_data


class GetTransactionsView(HTTPMethodView):

    async def post(self, request):
        json_request = request.json

        if 'email' not in json_request or 'password' not in json_request:
            return response.json({"error": {"message": "email/pass missing"}},
                                 status=422)

        user = await find_user_by_email(json_request['email'])

        if not user or 'data' not in user \
           or 'transactions_encrypted' not in user['data']:
            return response.json({
                'error': {'message': 'no such user'}
            }, status=422)

        data = decrypt_data(
            user['data']['transactions_encrypted'],
            json_request['password']
        )
        transactions = data['decrypted']

        logger.info(f"Decrypting transactions took {data['time_ms']}ms")

        if transactions is '':
            return response.json({
                'error': {'message': 'incorrect password'}}, status=422)

        return response.json({
            'email': user['email'],
            'id': str(user['_id']),
            'transactions': json.loads(transactions)
        })
