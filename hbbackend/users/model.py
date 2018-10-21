import hbbackend.commons


async def find_user_by_email(email):
    return await hbbackend.commons.db.users.find_one({'email': email})


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
