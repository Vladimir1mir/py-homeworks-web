import datetime
from typing import Annotated
import uuid
from fastapi import Depends, HTTPException, Header
from models import Session, Token
from config import TOKEN_TTL_SEC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]

async def get_token(x_token: Annotated[uuid.UUID, Header()],
                    session: SessionDependency) -> Token:
    query = select(Token).where(Token.token == x_token,
                                Token.creation_time
                                >= (datetime.datetime.now()
                                    - datetime.timedelta(seconds=TOKEN_TTL_SEC)))
    token = await session.scalar(query)
    if token is None:
        raise HTTPException(401, "Токен не найден.")
    return token

TokenDependency = Annotated[Token, Depends(get_token)]