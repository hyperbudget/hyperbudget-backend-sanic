from sanic import response
from sanic import Blueprint
from sanic.log import logger

import json

from hbbackend.users.model import find_user_by_email, update_user
from hbbackend.util.crypto import decrypt_data, encrypt_data


bp = Blueprint('transactions', url_prefix='/account/transactions')


@bp.post('/list')
async def get_transactions(request):
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


@bp.post('/update')
async def update_transactions(request):
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


@bp.options('/list')
def accept_options_list(request):
    return response.text('')


@bp.options('/update')
def accept_options_update(request):
    return response.text('')
