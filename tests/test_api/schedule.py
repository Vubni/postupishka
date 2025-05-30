import requests
from config import URL

def test_add_schedule(token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "content": "Понедельник: 10:00-12:00 Математика, 13:00-15:00 Русский"
    }
    response = requests.post(URL + "/schedule", json=data, headers=headers)
    assert response.status_code == 204, f"'/schedule' Ожидался статус 204, получен {response.status_code}"

def test_get_schedule(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/schedule", headers=headers)
    assert response.status_code == 200, f"'/schedule' Ожидался статус 200, получен {response.status_code}"
    assert isinstance(response.json(), list), "Неверная структура расписания"