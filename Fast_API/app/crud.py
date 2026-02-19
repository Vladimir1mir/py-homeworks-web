from models import ADVERT_OBJ, ADVERT_CLS, USER_OBJ, USER_CLS

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from fastapi import HTTPException


async def add_advert(session: AsyncSession, advert: ADVERT_OBJ):
    session.add(advert)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Wrong user")


async def get_advert_by_id(
    session: AsyncSession, orm_cls: ADVERT_CLS, advert_id: int
) -> ADVERT_OBJ:
    orm_obj = await session.get(orm_cls, advert_id)
    if orm_obj is None:
        raise HTTPException(status_code=404, detail="Advert not found")
    return orm_obj


async def get_advert_by_qs(
    session: AsyncSession, orm_cls: ADVERT_CLS, **query_string: dict
) -> ADVERT_OBJ:
    orm_obj = await session.execute(select(orm_cls).filter_by(**query_string))
    return orm_obj


async def delete_advert(advert: ADVERT_OBJ, session: AsyncSession):
    await session.delete(advert)
    await session.commit()


async def add_user(session: AsyncSession, user: USER_OBJ):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")


async def get_user_by_id(
    session: AsyncSession, orm_cls: USER_CLS, user_id: int
) -> USER_OBJ:
    user_obj = await session.get(orm_cls, user_id)
    if user_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj


async def delete_user(user: USER_OBJ, session: AsyncSession):
    await session.delete(user)
    await session.commit()
