import motor.motor_asyncio
import asyncio


def create_client(host='mongodb://localhost:27017/hyperbudget-dev',
                  io_loop=None):
    if not io_loop:
        io_loop = asyncio.get_event_loop()

    client = motor.motor_asyncio.AsyncIOMotorClient(
        host,
        io_loop=io_loop,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000
    )
    return client
