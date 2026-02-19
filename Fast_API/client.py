import requests

response = requests.post(url='http://127.0.0.1:8000/api/v1/advertisement',
                          json={"title": "test", 
                                "description": "test", 
                                "price": 100, 
                                "author_id": 1, 
                                "created_at": "2022-12-12 00:00:00"})
print(response.status_code)
print(response.json())


response = requests.get(url='http://127.0.0.1:8000/api/v1/advertisement/1')
print(response.status_code)
print(response.json())