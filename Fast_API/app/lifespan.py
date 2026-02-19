from fastapi import FastAPI
from models import init_orm, close_orm
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('START')
    await init_orm()
    yield
    print('STOP')
    await close_orm()
    