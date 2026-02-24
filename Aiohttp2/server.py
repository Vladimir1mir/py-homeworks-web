from datetime import datetime

import aiopg
import gino
from aiohttp import web
from asyncpg import UniqueViolationError

DB_DSN = f"postgres://username:password@127.0.0.1:5432/db_name"

db = gino.Gino()


class BaseModel:

    @classmethod
    async def get_or_404(cls, id_):
        instance = await cls.get(id_)
        if not instance:
            raise web.HTTPNotFound()
        return instance

    @classmethod
    async def create_instance(cls, **kwargs):
        try:
            instance = await cls.create(**kwargs)
            return instance
        except UniqueViolationError:
            raise web.HTTPBadRequest()


class Announcement(db.Model, BaseModel):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.DateTime, default=datetime.today)
    owner_fullname = db.Column(db.String, nullable=False)


class ServerStatus(web.View):

    async def get(self):
        return web.json_response({'status': 'ok'})


async def register_pg_pool(app):
    print('App start')
    async with aiopg.create_pool(DB_DSN) as pool:
        app['pg_pool'] = pool
        yield
    print('App finish')


async def register_orm(app):
    await db.set_bind(DB_DSN)
    yield
    await db.pop_bind().close()


class AnnouncementsView(web.View):
    async def get(self):
        pool = self.request.app['pg_pool']
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT * FROM announcements')
                db_response = await cursor.fetchall()
                return web.json_response(db_response)


class AnnouncementView(web.View):
    async def get(self):
        announcement_id = int(self.request.match_info['announcement_id'])
        announcement = await Announcement.get_or_404(announcement_id)
        return web.json_response(announcement.to_dict())

    async def post(self):
        announcement_data = await self.request.json()
        new_announcement = await Announcement.create_instance(**announcement_data)
        return web.json_response(new_announcement.to_dict())


app = web.Application()
app.add_routes([web.get('/status', ServerStatus)])
app.add_routes([web.get('/announcements', AnnouncementsView)])
app.add_routes([web.get('/announcement/{announcement_id:\d+}', AnnouncementView)])
app.add_routes([web.get('/announcement', AnnouncementView)])
app.cleanup_ctx.append(register_pg_pool)
app.cleanup_ctx.append(register_orm)
web.run_app(app, port=5001)
