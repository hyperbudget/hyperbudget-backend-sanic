async def find_user_by_email(mongo_db, email):
    return await mongo_db.users.find_one({'email': email})
