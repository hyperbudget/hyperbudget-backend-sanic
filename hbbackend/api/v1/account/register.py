from sanic import response, Blueprint
from sanic_validation import validate_json

import json

from hbbackend.users.model import create_user, find_user_by_email
from hbbackend.util.crypto import encrypt_data

bp = Blueprint('register', url_prefix='/account')

register_schema = {
    'firstname': {'type': 'string', 'required': True},
    'lastname': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
}


@bp.post('/register')
@validate_json(register_schema)
async def register(request):
    json_request = request.json

    user = await find_user_by_email(json_request['email'])

    if user:
        return response.json({'error': {"message": 'email taken'}},
                             status=422)

    data = encrypt_data(json.dumps([]), json_request['password'])

    id = await create_user(
        email=json_request['email'],
        settings=data['encrypted_b64'],
        transactions=data['encrypted_b64'],
        categories=data['encrypted_b64'],
        first_name=json_request['firstname'],
        last_name=json_request['lastname']
    )

    return response.json({
        'id': str(id)
    })


@bp.options('/register')
def accept_options(request):
    return response.text('')
