from sanic import response, Blueprint
from sanic_validation import validate_json

import hbbackend.users.model as model

bp = Blueprint('password_reset', url_prefix='/account')

reset_schema = {
    'token': {'type': 'string', 'required': True},
    'user_id': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}

request_reset_schema = {
    'email': {'type': 'string', 'required': True},
}


@bp.post('reset-password')
@validate_json(request_reset_schema)
async def request_reset(request):
    json_request = request.json

    user = await model.find_user_by_email(json_request['email'])

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

    data = await model.send_reset_email(user)

    if 'ok' in data and data['ok']:
        return response.json({
            'ok': True
        })
    else:
        return response.json({
            'ok': False
        }, status=422)


@bp.post('/account/confirm-reset-password')
@validate_json(reset_schema)
async def do_reset_password(request):
    req = request.json

    user = await model.find_user_by_id(req['user_id'])

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

    token_is_correct = await model.check_token(user, req['token'])

    if token_is_correct:
        await model.reset_encrypted_data(user, req['password'])

        return response.json({
            'ok': True,
            'user': {
                'id': str(user['_id']),
                'email': user['email']
            }
        })
    else:
        return response.json({
            'ok': False,
            'error': {'message': 'Could not verify details'}
        }, status=422)
