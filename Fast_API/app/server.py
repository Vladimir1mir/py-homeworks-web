from fastapi import FastAPI, Query
import uvicorn
from lifespan import lifespan
from models import Advert, User
from dependency import SessionDependency
import crud
from constants import STATUS_DELETED
from fastapi.middleware.cors import CORSMiddleware

from schema import (
    GetAdvertisementResponse,
    CreateAdvertisementResponse,
    CreateAdvertisementRequest,
    UpdateAdvertisementRequest,
    UpdateAdvertisementResponse,
    DeleteAdvertisementResponse,
    CreateUserResponse,
    CreateUserRequest,
    GetUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    DeleteUserResponse,
)


app = FastAPI(
    title="Advertisement API",
    version="0.1.0",
    description="API for advertisement",
    lifespan=lifespan,
)


@app.post(
    "/api/v1/advertisement",
    response_model=CreateAdvertisementResponse,
    tags=["advertisements"],
)
async def create_advertisement(
    advert_request: CreateAdvertisementRequest, session: SessionDependency
):
    advertisement_obj = Advert(
        title=advert_request.title,
        description=advert_request.description,
        price=advert_request.price,
        author_id=advert_request.author_id,
    )
    await crud.add_advert(session, advertisement_obj)
    return advertisement_obj.id_dict


@app.patch(
    "/api/v1/advertisement/{advertisement_id}",
    response_model=UpdateAdvertisementResponse,
    tags=["advertisements"],
)
async def update_advertisement(
    advertisement_id: int,
    advertisement_request: UpdateAdvertisementRequest,
    session: SessionDependency,
):

    advertisement_json = advertisement_request.model_dump(exclude_unset=True)
    advertisement = await crud.get_advert_by_id(session, Advert, advertisement_id)
    for field, value in advertisement_json.items():
        setattr(advertisement, field, value)

    await crud.add_advert(session, advertisement)
    return advertisement.id_dict


@app.delete(
    "/api/v1/advertisement/{advertisement_id}",
    response_model=DeleteAdvertisementResponse,
    tags=["advertisements"],
)
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement = await crud.get_advert_by_id(session, Advert, advertisement_id)
    await crud.delete_advert(advertisement, session)
    return STATUS_DELETED


@app.get(
    "/api/v1/advertisement/{advertisement_id}",
    response_model=GetAdvertisementResponse,
    tags=["advertisements"],
)
async def get_advertisement(session: SessionDependency, advertisement_id: int):
    advertisement_obj = await crud.get_advert_by_id(session, Advert, advertisement_id)
    return advertisement_obj.dict


@app.get(
    "/api/v1/advertisement",
    response_model=list[GetAdvertisementResponse],
    tags=["advertisements"],
)
async def get_advertisement_by_qs(
    session: SessionDependency,
    title: str = Query(None),
    description: str = Query(None),
    price: int = Query(None),
    author_id: int = Query(None),
):
    query_string = {}
    if title:
        query_string["title"] = title
    if description:
        query_string["description"] = description
    if price:
        query_string["price"] = price
    if author_id:
        query_string["author_id"] = author_id

    advertisement_obj = await crud.get_advert_by_qs(session, Advert, **query_string)
    advertisement_list = [
        advert.dict for advert in advertisement_obj.unique().scalars().all()
    ]
    return advertisement_list


@app.post("/api/v1/user", response_model=CreateUserResponse, tags=["users"])
async def create_user(user_request: CreateUserRequest, session: SessionDependency):
    user_obj = User(name=user_request.name, password=user_request.password)
    await crud.add_user(session, user_obj)
    return user_obj.id_dict


@app.get("/api/v1/user/{user_id}", response_model=GetUserResponse, tags=["users"])
async def get_user(session: SessionDependency, user_id: int):
    user_obj = await crud.get_user_by_id(session, User, user_id)
    return user_obj.dict


@app.patch("/api/v1/user/{user_id}", response_model=UpdateUserResponse, tags=["users"])
async def update_user(
    user_id: int, user_request: UpdateUserRequest, session: SessionDependency
):

    user_json = user_request.model_dump(exclude_unset=True)
    user = await crud.get_user_by_id(session, User, user_id)
    for field, value in user_json.items():
        setattr(user, field, value)

    await crud.add_user(session, user)
    return user.id_dict


@app.delete("/api/v1/user/{user_id}", response_model=DeleteUserResponse, tags=["users"])
async def delete_user(user_id: int, session: SessionDependency):
    user = await crud.get_user_by_id(session, User, user_id)
    await crud.delete_user(user, session)
    return STATUS_DELETED


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
