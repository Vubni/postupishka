import requests
from config import URL

def test_create_user():
    data = {
        "password": "123123",
        "class_number": 10,
        "email": "testtest@vubni.com",
        "first_name": "Test"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 201, f"'/reg' Выполнено 0/6 тестов, ожидается статус 201, получен {response.status_code}"
    assert "token" in response.json(), f"'/reg' Выполнено 0/6 тестов, ожидается наличие параметра 'token' в ответе"
    
    data = {
        "password": "123",
        "class_number": 10,
        "email": "testtest@vubni.com",
        "first_name": "Test1"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 409, f"'/reg' Выполнено 1/6 тестов, ожидается статус 409, получен {response.status_code}"
    
    data = {
        "password": "123",
        "class_number": 10,
        "email": "testtest@vubni.com",
        "first_name": "Test"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 409, f"'/reg' Выполнено 2/6 тестов, ожидается статус 409, получен {response.status_code}"
    
    data = {
        "password": "123123",
        "class_number": 10,
        "email": "testtest@vubn235235235.ru",
        "first_name": "string"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 400, f"'/reg' Выполнено 3/6 тестов, ожидается статус 400, получен {response.status_code}"
    
    data = {
        "password": "123123",
        "class_number": 13,
        "email": "testte@vubni.com",
        "first_name": "string"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 400, f"'/reg' Выполнено 4/6 тестов, ожидается статус 400, получен {response.status_code}"
    
    data = {
        "password": 435345,
        "class_number": 10,
        "email": "testte@vubni.com",
        "first_name": "string"
    }
    response = requests.post(URL + "/reg", json=data)
    assert response.status_code == 400, f"'/reg' Выполнено 5/6 тестов, ожидается статус 400, получен {response.status_code}"
    
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
    
def test_tg(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(URL + "/telegram/url", headers=headers)
    assert response.status_code == 200, f"'/telegram/url' Выполнено 0/1 тестов, ожидается статус 200, получен {response.status_code}"
    
def test_edit(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    data = {"subjects": [{"subject": "Русский язык", "current_score": 20, "desired_score": 90},
                         {"subject": "Математика", "current_score": 10, "desired_score": 100}
                         ]}
    response = requests.patch(URL + "/profile", json=data, headers=headers)
    assert response.status_code == 204, f"'/profile' Выполнено 0/1 тестов, ожидается статус 204, получен {response.status_code}"
    
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(URL + "/profile", headers=headers)
    assert response.status_code == 200, f"'/profile' Выполнено 0/4 тестов, ожидается статус 200, получен {response.status_code}"
    res = response.json()
    assert len(res["subjects"]) == 2, f"'/profile' Выполнено 1/4 тестов, ожидается 2 объекта в 'subjects', получен " + res["subjects"]
    assert res["subjects"][0]["subject"] == "Русский язык", f"'/profile' Выполнено 2/4 тестов, ожидается статус 200, получен " + res["subjects"][0]["subject"]
    assert res["subjects"][1]["subject"] == "Математика", f"'/profile' Выполнено 3/4 тестов, ожидается статус 200, получен" + res["subjects"][1]["subject"]
    
def delete_profile(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.delete(URL + "/profile", headers=headers)
    assert response.status_code == 204, f"'/reg' Выполнено 0/6 тестов, ожидается статус 204, получен {response.status_code}"
