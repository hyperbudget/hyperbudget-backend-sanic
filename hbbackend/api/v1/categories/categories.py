from sanic import response
from sanic.log import logger
from sanic import Blueprint

import json

from hbbackend.users.model import find_user_by_email, update_user
from hbbackend.util.crypto import decrypt_data, encrypt_data
from hbbackend.commons import default_categories


bp = Blueprint('categories', url_prefix='/account/categories')


@bp.post('/list')
async def get_categories(request):
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
    # Well, I call it that, but is it really?
    # Isn't it kind of nice to avoid doing json decoding work
    # until the last minute? It's really not that bad.
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


@bp.post('/update')
async def update_categories(request):
    json_request = request.json

    if 'email' not in json_request or 'password' not in json_request \
            or 'categories' not in json_request:
        return response.json({"error": {'message': "data missing"}},
                             status=422)

    user = await find_user_by_email(json_request['email'])

    if not user or 'settings' not in user:
        return response.json({'error': {"message": 'no such user'}},
                             status=422)

    data = decrypt_data(
        user['settings'],
        json_request['password']
    )
    settings = data['decrypted']

    logger.info(f'Decrypting settings took {data["time_ms"]}ms')

    if settings is '':
        return response.json({'error': {"message": 'incorrect password'}},
                             status=422)

    data = encrypt_data(
        json.dumps(json_request['categories']),
        json_request['password']
    )

    logger.info(f'Encrypting categories took {data["time_ms"]}ms')

    await update_user(
        json_request['email'],
        {
            'preferences': {
                'categories_encrypted': data['encrypted_b64']
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
