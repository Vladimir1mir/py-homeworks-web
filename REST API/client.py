import requests

# Создание пользователя
# print("Создание двух пользователей и одного админа")
# data = requests.post("http://127.0.0.1:8000/user", json={"name": "user_1", "password": "12345678"})
# print(data.status_code)
# # print(data.json())
# data = requests.post("http://127.0.0.1:8000/user", json={"name": "user_2", "password": "67891012"})
# print(data.status_code)
# # print(data.json())
# data = requests.post("http://127.0.0.1:8000/user", json={"name": "admin",
#                                                                 "password": "admin12345678",
#                                                                 "role": "admin"})
# print(data.status_code)
# # print(data.json())
# print()
# print("Повтор создание первого пользователя")
# data = requests.post("http://127.0.0.1:8000/user", json={"name": "user_1", "password": "user12345678"})
# print(data.status_code)
# print(data.json())
# print("Создание пользователя с неподходящим паролем")
# data = requests.post("http://127.0.0.1:8000/user", json={"name": "user_3", "password": "12345"})
# print(data.status_code)
# print(data.json())
# print()
#
#
# # Авторизация пользователей с получением токена
# print("Авторизация")
# data = requests.post("http://127.0.0.1:8000/login", json={"name": "user_1", "password": "user12345678"})
# print(data.status_code)
# print(data.json())
# token_user1 = data.json()["token"]
# data = requests.post("http://127.0.0.1:8000/login", json={"name": "user_2", "password": "12345678"})
# print(data.status_code)
# print(data.json())
# token_user2 = data.json()["token"]
# data = requests.post("http://127.0.0.1:8000/login", json={"name": "admin", "password": "admin12345678"})
# print(data.status_code)
# print(data.json())
# token_admin = data.json()["token"]
# print()
#
# print("Авторизация с неверными данными")
# data = requests.post("http://127.0.0.1:8000/login", json={"name": "user", "password": "user12345678"})
# print(data.status_code)
# print(data.json())
# data = requests.post("http://127.0.0.1:8000/login", json={"name": "admin", "password": "12345678"})
# print(data.status_code)
# print(data.json())
# print()
#
# # Обновление данных только своих или admin
# print("Обновление данных пользователя")
# data = requests.patch("http://127.0.0.1:8000/user/1", json={"name": "user1", "password": "user12345678"},
#                       headers={"x-token": token_user1})
# print(data.status_code)
# print(data.json())
# data = requests.patch("http://127.0.0.1:8000/user/1", json={"name": "USER_1", "password": "user12345678"},
#                       headers={"x-token": token_admin})
# print(data.status_code)
# print(data.json())
# print()
# print("Обновление данных без прав")
# data = requests.patch("http://127.0.0.1:8000/user/1", json={"name": "user1", "password": "user12345678"})
# print(data.status_code)
# print(data.json())
# data = requests.patch("http://127.0.0.1:8000/user/1", json={"name": "user1", "password": "user12345678"},
#                       headers={"x-token": token_user2})
# print(data.status_code)
# print(data.json())
# print()
#
# # Создание объявлений
# print("Создание своего объявления")
# data = requests.post("http://127.0.0.1:8000/advertisement",
#                      json={"title": "объявление1", "description": "содержание объявление", "price": "555"},
#                      headers={"x-token": token_user1})
# print(data.status_code)
# print(data.json())
# data = requests.post("http://127.0.0.1:8000/advertisement",
#                      json={"title": "объявление2", "description": "содержание объявление", "price": "555"},
#                      headers={"x-token": token_user1})
# print(data.status_code)
# print(data.json())
# print()
# print("Создание объявления неавторизованным пользователем")
# data = requests.post("http://127.0.0.1:8000/advertisement",
#                      json={"title": "объявление", "description": "содержание объявление", "price": "555"})
# print(data.status_code)
# print(data.json())
# print()
#
# # Обновление объявления
# print("Обновление объявления автором и админом")
# data = requests.patch("http://127.0.0.1:8000/advertisement/1",
#                       json={"title": "объявление", "description": "обновлённое объявление", "price": "555"},
#                       headers={"x-token": token_user1})
# print(data.status_code)
# print(data.json())
# data = requests.patch("http://127.0.0.1:8000/advertisement/1",
#                       json={"title": "новое_объявление"},
#                       headers={"x-token": token_admin})
# print(data.status_code)
# print(data.json())
#
# print("Обновление объявления неавторизованным пользователем и  чужого объявления")
# data = requests.patch("http://127.0.0.1:8000/advertisement/1",
#                       json={"title": "объявление", "description": "обновлённое объявление", "price": "555"})
# print(data.status_code)
# print(data.json())
# data = requests.patch("http://127.0.0.1:8000/advertisement/1",
#                       json={"title": "new_объявление"},
#                       headers={"x-token": token_user2})
# print(data.status_code)
# print(data.json())
# print()
#
# # Получение объявлений
# print("Получение объявлений")
# data = requests.get("http://127.0.0.1:8000/advertisement/1")
# print(data.status_code)
# print(data.json())
# print("Получение не существующего объявления")
# data = requests.get("http://127.0.0.1:8000/advertisement/9")
# print(data.status_code)
# print(data.json())
# print()
#
# # Поиск объявлений
# print("Поиск объявлений")
# data = requests.get("http://127.0.0.1:8000/advertisement", params={"user_id": 1})
# print(data.status_code)
# print(data.json())
# print(len(data.json()["results"]) == 2)
# print()
#
# # Удаление объявления
# print("Удаление неавторизованным пользователем")
# data = requests.delete("http://127.0.0.1:8000/advertisement/1")
# print(data.status_code)
# print(data.json())
# print("Удаление чужого объявления")
# data = requests.delete("http://127.0.0.1:8000/advertisement/1", headers={"x-token": token_user2})
# print(data.status_code)
# print(data.json())
# print("Удаление несуществующего объявления")
# data = requests.delete("http://127.0.0.1:8000/advertisement/5", headers={"x-token": token_admin})
# print(data.status_code)
# print(data.json())
#
# print("Удаление своего объявления")
# data = requests.delete("http://127.0.0.1:8000/advertisement/1", headers={"x-token": token_user1})
# print(data.status_code)
# print(data.json())
# print("Удаление объявления админом")
# data = requests.delete("http://127.0.0.1:8000/advertisement/2", headers={"x-token": token_admin})
# print(data.status_code)
# print(data.json())
# print()
#
# # Получение пользователя
# print("Получение пользователя")
# data = requests.get("http://127.0.0.1:8000/user/1")
# print(data.status_code)
# print(data.json())
# print("Получение не существующего пользователя")
# data = requests.get("http://127.0.0.1:8000/user/9")
# print(data.status_code)
# print(data.json())
# print()
#
# # Удаление пользователя
# print("Удаление несуществующего пользователя")
# data = requests.delete("http://127.0.0.1:8000/user/5", headers={"x-token": token_admin})
# print(data.status_code)
# print(data.json())
# print("Удаление пользователя неавторизованным пользователем")
# data = requests.delete("http://127.0.0.1:8000/user/1")
# print(data.status_code)
# print(data.json())
# print("Удаление чужого пользователя")
# data = requests.delete("http://127.0.0.1:8000/user/1", headers={"x-token": token_user2})
# print(data.status_code)
# print(data.json())
#
# print("Успешное удаление пользователя")
# data = requests.delete("http://127.0.0.1:8000/user/1", headers={"x-token": token_user1})
# print(data.status_code)
# print(data.json())
# data = requests.delete("http://127.0.0.1:8000/user/2", headers={"x-token": token_admin})
# print(data.status_code)
# print(data.json())