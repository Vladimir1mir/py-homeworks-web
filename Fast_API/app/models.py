import datetime

from sqlalchemy import DateTime, Integer, String, Text, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from config import POSTGRES_DSN


engine = create_async_engine(POSTGRES_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    @property
    def id_dict(self):
        return {"id": self.id}


class User(Base):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    adverts = relationship(
        "Advert",
        back_populates="author",
        cascade="all, delete",
        passive_deletes=True,
        lazy="joined",
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "registration_time": self.registration_time.isoformat(),
        }


class Advert(Base):

    __tablename__ = "advert"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    price: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    author = relationship("User", back_populates="adverts", lazy="joined")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "created_at": self.created_at.isoformat(),
            "author_id": self.author_id,
            "author_name": self.author.name,
        }


ADVERT_OBJ = Advert
ADVERT_CLS = type[Advert]
USER_OBJ = User
USER_CLS = type[User]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
