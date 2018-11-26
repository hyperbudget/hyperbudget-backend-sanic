from sanic import response
from sanic.views import HTTPMethodView
from sanic_validation import validate_json

from hbbackend.users.model import find_user_by_email, send_reset_email


class PwdResetView(HTTPMethodView):
    reset_schema = {
        'email': {'type': 'string', 'required': True},
    }

    @staticmethod
    @validate_json(reset_schema)
    async def post(request):
        json_request = request.json

        if 'email' not in json_request:
            return response.json({"error": {"message": "email missing"}},
                                 status=422)

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

        data = await send_reset_email(user)

        if 'ok' in data and data['ok']:
            return response.json({
                'ok': True
            })
        else:
            print("Could not send reset email: ", data)
            return response.json({
                'ok': False
            }, status=422)
