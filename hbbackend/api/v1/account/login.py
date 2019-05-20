from sanic import response, Blueprint
from sanic_validation import validate_json

import json

from hbbackend.users.model import find_user_by_email
from hbbackend.util.crypto import decrypt_data

bp = Blueprint('login', url_prefix='/account')

login_schema = {
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}


@bp.post('login')
@validate_json(login_schema)
async def post(self, request):
    json_request = request.json

    user = await find_user_by_email(json_request['email'])

    if not user or 'settings' not in user:
        return response.json(
            {
                'error': {
                    "message": 'no such user',
                    "type": "auth"
                },
            },
            status=422
        )

    data = decrypt_data(user['settings'], json_request['password'])
    settings = data['decrypted']

    if settings is '':
        return response.json(
            {
                'error': {
                        "message": 'incorrect password',
                        "type": "auth"
                }
            },
            status=422)

    return response.json({
        'email': user['email'],
        'id': str(user['_id']),
        'settings': json.loads(settings),
        'first_name': user.get('first_name')
    })
