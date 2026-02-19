import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
import datetime



POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", '123345')
POSTGRES_USER = os.getenv("POSTGRES_USER", 'postgres')
POSTGRES_DB = os.getenv("POSTGRES_DB", 'app')
POSTGRES_HOST = os.getenv("POSTGRES_HOST", '127.0.0.1')
POSTGRES_PORT = os.getenv("POSTGRES_PORT", '5431')


PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN, pool_pre_ping=True)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    time_of_creation: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(100), index=True, nullable=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'time_of_creation': self.time_of_creation.isoformat(),
            'owner': self.owner,
        }



Base.metadata.create_all(bind=engine)

