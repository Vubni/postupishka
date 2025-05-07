import requests
from config import URL

def test_create_user():
    data = {
        "password": "123123",
        "class": 10,
        "email": "testtest@vubni.com",
        "firstName": "Test"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 201, f"'/reg' Выполнено 0/6 тестов, ожидается статус 201, получен {response.status_code}"
    assert "token" in response.json(), f"'/reg' Выполнено 0/6 тестов, ожидается наличие параметра 'token' в ответе"
    
    data = {
        "password": "123",
        "class": 10,
        "email": "testtest@vubni.com",
        "firstName": "Test1"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 409, f"'/reg' Выполнено 1/6 тестов, ожидается статус 409, получен {response.status_code}"
    
    data = {
        "password": "123",
        "class": 10,
        "email": "testtest@vubni.com",
        "firstName": "Test"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 409, f"'/reg' Выполнено 2/6 тестов, ожидается статус 409, получен {response.status_code}"
    
    data = {
        "password": "123123",
        "class": 10,
        "email": "testtest@vubn235235235.ru",
        "firstName": "string"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 422, f"'/reg' Выполнено 3/6 тестов, ожидается статус 422, получен {response.status_code}"
    
    data = {
        "password": "123123",
        "class": 13,
        "email": "testte@vubni.com",
        "firstName": "string"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 400, f"'/reg' Выполнено 4/6 тестов, ожидается статус 400, получен {response.status_code}"
    assert "name" in response.json() and "error" in response.json(), f"'/reg' Выполнено 4/6 тестов, ожидается наличие параметров 'name' и 'error' в ответе"
    assert response.json()["name"] == "class", f"'/reg' Выполнено 4/6 тестов, ожидается значение 'class' в параметре 'name' в ответе"
    
    data = {
        "password": 435345,
        "class": 10,
        "email": "testte@vubni.com",
        "firstName": "string"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 400, f"'/reg' Выполнено 5/6 тестов, ожидается статус 400, получен {response.status_code}"
    assert "name" in response.json() and "error" in response.json(), f"'/reg' Выполнено 5/6 тестов, ожидается наличие параметров 'name' и 'error' в ответе"
    assert response.json()["name"] == "password", f"'/reg' Выполнено 6/6 тестов, ожидается значение 'password' в параметре 'name' в ответе"
    
def test_auth():
    data = {
        "identifier": "testtest@vubni.com",
        "password": "123123",
    }
    response = requests.post(URL + "/auth", json=data)
    assert response.status_code == 200, f"'/auth' Выполнено 0/1 тестов, ожидается статус 200, получен {response.status_code}"
    assert "token" in response.json(), f"'/auth' Выполнено 0/1 тестов, ожидается наличие параметра 'token' в ответе"
    token = response.json()["token"]
    return token
    

def test_profile(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(URL + "/profile", headers=headers)
    assert response.status_code == 200, f"'/profile' Выполнено 0/1 тестов, ожидается статус 200, получен {response.status_code}"
    print(response.json())
    
def test_tg(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(URL + "/telegram/url", headers=headers)
    assert response.status_code == 200, f"'/telegram/url' Выполнено 0/1 тестов, ожидается статус 200, получен {response.status_code}"
    
    
def delete_profile(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.delete(URL + "/profile", headers=headers)
    assert response.status_code == 204, f"'/reg' Выполнено 0/6 тестов, ожидается статус 204, получен {response.status_code}"