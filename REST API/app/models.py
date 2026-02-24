import datetime
import uuid
from decimal import Decimal
from sqlalchemy import DateTime, Integer, String, func, Numeric, UUID, ForeignKey
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import config
from custom_type import ROLE

engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {"id": self.id}


class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, server_default=func.gen_random_uuid())
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates="tokens")

    @property
    def dict(self):
        return {"token": self.token}


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[ROLE] = mapped_column(String, default="user")
    tokens: Mapped[list["Advertisement"]] = relationship(Token, lazy="joined",
                                                         back_populates="user",
                                                         cascade="all, delete-orphan")
    advertisements: Mapped[list["Advertisement"]] = relationship("Advertisement",
                                                                 lazy="joined",
                                                                 back_populates="user",
                                                                 cascade="all, delete-orphan")

    @property
    def dict(self):
        return {"id": self.id, "name": self.name}


class Adv(Base):
    __tablename__ = "advertisement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=12, scale=2))
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates="advertisements")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "creation_time": self.creation_time.strftime("%d %B %Y %H:%M"),
            "user_id": self.user_id
        }


ORM_OBJ = Adv | User | Token
ORM_CLS = type[Adv] | type[User] | type[Token]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()