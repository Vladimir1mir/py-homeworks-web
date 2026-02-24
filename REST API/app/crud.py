from models import ORM_CLS, ORM_OBJ
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy import select


async def get_item_by_id(session: AsyncSession, orm_cls, item_id: int) -> ORM_OBJ:
    orm_obj = await session.get(orm_cls, item_id)
    if orm_obj is None:
        raise HTTPException(404, f"Item not found")
    return orm_obj

async def add_item(session: AsyncSession, item: ORM_OBJ):

    session.add(item)
    try:
        await session.commit()

    except IntegrityError as err:
        raise HTTPException(409, f"Item already exists")

async def delete_item(session: AsyncSession, item: ORM_OBJ):
    await session.delete(item)
    await session.commit()

async def get_advert_by_qs(
    session: AsyncSession, orm_cls: ORM_CLS, **query_string: dict
) -> ORM_OBJ:
    orm_obj = await session.execute(select(orm_cls).filter_by(**query_string))
    return orm_obj