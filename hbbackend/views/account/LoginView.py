from sanic import response
from sanic.views import HTTPMethodView
import json

from hbbackend.users.model import find_user_by_email
from hbbackend.util.crypto import decrypt_data


class LoginView(HTTPMethodView):

    async def post(self, request):
        json_request = request.json

        if 'email' not in json_request or 'password' not in json_request:
            return response.json({"error": {"message": "email/pass missing"}},
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
            'settings': json.loads(settings)
        })
