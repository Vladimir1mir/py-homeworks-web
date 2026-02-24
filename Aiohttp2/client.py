import asyncio
from aiohttp import ClientSession


async def check_status():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:5001/status') as resp:
            return await resp.json()


async def get_announcements():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:5001/announcements') as resp:
            return await resp.json()


async def get_announcement():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:5001/announcement/1') as resp:
            return await resp.json()


async def create_announcement():
    async with ClientSession() as session:
        async with session.post('http://127.0.0.1:5001/announcement', json={
            "title": "new title",
            "description": "new description",
            "created": "new date",
            "owner_fullname": "new owner"
        }) as resp:
            return await resp.text()


async def delete_announcement():
    async with ClientSession() as session:
        async with session.delete('http://127.0.0.1:5001/announcement/2') as resp:
            return await resp.text()


async def main():
    response = await check_status()
    print(response)
    response = await get_announcements()
    print(response)
    response = await get_announcement()
    print(response)
    response = await create_announcement()
    print(response)
    response = await delete_announcement()
    print(response)


asyncio.run(main())
