from sanic import response
from sanic.views import HTTPMethodView
from sanic_validation import validate_json

import hbbackend.users.model as model


class DoResetView(HTTPMethodView):
    reset_schema = {
        'token': {'type': 'string', 'required': True},
        'email': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True}
    }

    @staticmethod
    @validate_json(reset_schema)
    async def post(request):
        req = request.json

        user = await model.find_user_by_email(req['email'])

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
                'ok': True
            })
        else:
            return response.json({
                'ok': False
            }, status=422)
