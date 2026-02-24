from fastapi import FastAPI, HTTPException

from dependency import SessionDependency, TokenDependency
from constans import SUCCESS_RESPONSE
from lifespan import lifespan
from sqlalchemy import select, and_
from schema import (CreateAdvertisementRequest, UpdateAdvertisementRequest,
                    CreateAdvertisementResponse, UpdateAdvertisementResponse,
                    SearchAdvertisementResponse, DeleteAdvertisementResponse,
                    GetAdvertisementResponse, LoginResponse, LoginRequest,
                    CreateUserResponse, CreateUserRequest, GetUserResponse,
                    DeleteUserResponse, UpdateUserRequest, UpdateUserResponse)
import models
import crud
from auth import hash_password, check_password

app = FastAPI(title="Advertisement API",
              description="Advertisement app",
              lifespan=lifespan)


# создание пользователя
@app.post("/user", tags=["user"], response_model=CreateUserResponse)
async def create_user(user_data: CreateUserRequest, session: SessionDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = hash_password(user_dict["password"])
    user_orm_obj = models.User(**user_dict)
    await crud.add_item(session, user_orm_obj)
    return user_orm_obj.id_dict


# получение токена
@app.post("/login", tags=["user"], response_model=LoginResponse)
async def login(login_data: LoginRequest, session: SessionDependency):
    query = select(models.User).where(models.User.name == login_data.name)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(401, "Неверные данные.")
    if not check_password(login_data.password, user.password):
        raise HTTPException(401, "Неверные данные.")
    token = models.Token(user_id=user.id)
    await crud.add_item(session, token)
    return token.dict


# получение пользователя по id
@app.get("/user/{user_id}", tags=["user"], response_model=GetUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)
    return user_orm_obj


# получение объявления по id
@app.get("/advertisement/{ad_id}", tags=["advertisement"],
         response_model=GetAdvertisementResponse)
async def get_advertisement(ad_id: int, session: SessionDependency):
    add_orm_obj = await crud.get_item_by_id(session, models.Adv, ad_id)
    return add_orm_obj.dict


# поиск объявление по полям
@app.get("/advertisement", tags=["advertisement"],
         response_model=SearchAdvertisementResponse)
async def get_advertisement(session: SessionDependency, title: str = None, description: str = None,
                            price: float = None, user_id: int = None):
    conditions = []
    if title:
        conditions.append(models.Adv.title == title)
    if description:
        conditions.append(models.Adv.description == description)
    if price:
        conditions.append(models.Adv.price == price)
    if user_id:
        conditions.append(models.Adv.user_id == user_id)
    query = select(models.Adv).where(and_(*conditions)).limit(10000)
    advertisements = await session.execute(query)
    advertisements = advertisements.scalars().unique().all()
    return {"results": [advertisement.dict for advertisement in advertisements]}


# обновление своих данных
@app.patch("/user/{user_id}", tags=["user"], response_model=UpdateUserResponse)
async def update_user(user_data: UpdateUserRequest,
                      user_id: int,
                      session: SessionDependency,
                      token: TokenDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    if token.user.role == "admin" or user_id == token.user_id:
        user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)
        for field, value in user_dict.items():
            setattr(user_orm_obj, field, value)
        await crud.add_item(session, user_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Недостаточно прав.")


# удаление себя или удаление администратором
@app.delete("/user/{user_id}", tags=["user"], response_model=DeleteUserResponse)
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    if token.user.role == "admin" or user_id == token.user_id:
        user_orm_obj = await crud.get_item_by_id(session, models.User, user_id)
        await crud.delete_item(session, user_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Недостаточно прав.")


# создание своего объявления
@app.post("/advertisement", tags=["advertisement"],
          response_model=CreateAdvertisementResponse)
async def create_advertisement(ad_data: CreateAdvertisementRequest,
                               session: SessionDependency,
                               token: TokenDependency):
    add_dict = ad_data.model_dump(exclude_unset=True)
    add_orm_obj = models.Adv(**add_dict, user_id=token.user_id)
    await crud.add_item(session, add_orm_obj)
    return add_orm_obj.id_dict


# обновление своего объявление или администратором
@app.patch("/advertisement/{ad_id}", tags=["advertisement"],
           response_model=UpdateAdvertisementResponse)
async def update_advertisement(ad_data: UpdateAdvertisementRequest,
                               ad_id: int, session: SessionDependency,
                               token: TokenDependency):
    add_dict = ad_data.model_dump(exclude_unset=True)
    add_orm_obj = await crud.get_item_by_id(session, models.Adv, ad_id)
    if token.user.role == "admin" or add_orm_obj.user_id == token.user_id:
        for field, value in add_dict.items():
            setattr(add_orm_obj, field, value)
        await crud.add_item(session, add_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Недостаточно прав.")


# удаление своего объявления или удаление администратором
@app.delete("/advertisement/{ad_id}", tags=["advertisement"],
            response_model=DeleteAdvertisementResponse)
async def delete_advertisement(ad_id: int, session: SessionDependency, token: TokenDependency):
    add_orm_obj = await crud.get_item_by_id(session, models.Adv, ad_id)
    if token.user.role == "admin" or add_orm_obj.user_id == token.user_id:
        await crud.delete_item(session, add_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(403, "Недостаточно прав.")