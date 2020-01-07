import aiohttp
import json
from bson.objectid import ObjectId


import hbbackend.commons
from hbbackend.util.crypto import encrypt_data


async def find_user_by_email(email):
    return await hbbackend.commons.db.users.find_one({'email': email})


async def find_user_by_id(id):
    print(id)
    return await hbbackend.commons.db.users.find_one({'_id': ObjectId(id)})


async def update_user(email, data):
    user = await find_user_by_email(email)
    if not user:
        raise ValueError("User not found")

    return await hbbackend.commons.db.users.update_one(
        {'email': email},
        {'$set': data}
    )


async def create_user(**kwargs):
    result = await hbbackend.commons.db.users.insert_one({
        'email': kwargs['email'],
        'settings': kwargs['settings'],
        'firstName': kwargs['first_name'],
        'lastName': kwargs['last_name'],
        'data': {'transactions_encrypted': kwargs['transactions']},
        'preferences': {'categories_encrypted': kwargs['categories']},
    })

    return result.inserted_id


async def send_reset_email(user):
    service_url = hbbackend.commons.services['PWD_RESET_SERVICE']
    key = hbbackend.commons.api_keys['PWD_RESET_SERVICE_KEY']

    async with aiohttp.ClientSession() as client:
        async with client.post(
            f"{service_url}/email/send",
            json={
                "email": user['email'],
                "userId": str(user['_id']),
                "name": f"{user.get('firstName')} {user.get('lastName')}"
            },
            headers={'x-aws-key': key}
        ) as r:
            return await r.json()


async def check_token(user, token):
    service_url = hbbackend.commons.services['PWD_RESET_SERVICE']
    key = hbbackend.commons.api_keys['PWD_RESET_SERVICE_KEY']

    async with aiohttp.ClientSession() as client:
        async with client.post(
            f"{service_url}/token/verify",
            json={
                "userId": str(user['_id']),
                "token": token
            },
            headers={'x-aws-key': key}
        ) as r:
            json_response = await r.json()
            return 'correct' in json_response and json_response['correct']


async def reset_encrypted_data(user, password):
    data = encrypt_data(json.dumps([]), password)

    return await update_user(
        email=user['email'],
        data={
            'settings': data['encrypted_b64'],
            'transactions': data['encrypted_b64'],
            'categories': data['encrypted_b64'],
            'data': {'transactions_encrypted': data['encrypted_b64']},
            'preferences': {'categories_encrypted': data['encrypted_b64']},
        }
    )
