import requests
from config import URL

def test_send_question(token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"question": "Как справиться со стрессом?"}
    response = requests.post(URL + "/psychologist", json=data, headers=headers)
    assert response.status_code == 200, f"'/psychologist' Ожидался статус 200, получен {response.status_code}"
    assert "answer" in response.json(), "Ответ от психолога отсутствует"

def test_get_dialog(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/psychologist", headers=headers)
    assert response.status_code == 200, f"'/psychologist' Ожидался статус 200, получен {response.status_code}"
    assert isinstance(response.json(), list), "Ожидался массив сообщений"