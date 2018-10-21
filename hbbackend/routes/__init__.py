from sanic import response

from hbbackend.users.model import find_user_by_email
import hbbackend.commons


def setup_routes(app):
    @app.route("/")
    async def index(request):
        return response.json({"hello": "world"})

    @app.route("/login", methods=["POST"])
    async def login(request):
        json_request = request.json

        if 'email' not in json_request:
            return response.json({"error": "email missing"}, status=422)

        user = await find_user_by_email(hbbackend.commons.db,
                                        json_request['email'])

        if (user):
            return response.json({
                'email': user['email'],
                'id': str(user['_id'])
            })
        else:
            return response.json({'error': 'no such user'}, status=422)
