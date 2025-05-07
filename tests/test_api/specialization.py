import requests
from config import URL

def generate_question(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(URL + "/specialization/question", headers=headers)
    assert response.status_code == 200, f"'/specialization/question' Выполнено 0/1 тестов, ожидается статус 200, получен {response.status_code}"
    assert "question" in response.json(), f"'/specialization/question' Выполнено 0/1 тестов, ожидается наличие параметра 'question' в ответе"
    assert "counts_remaind" in response.json(), f"'/specialization/question' Выполнено 0/1 тестов, ожидается наличие параметра 'counts_remaind' в ответе"
    return response.json()
    
def answer(token, content):
    headers = {
        "Authorization": "Bearer " + token,
    }
    data = {"answer": content}
    response = requests.post(URL + "/specialization/answer", json=data, headers=headers)
    assert response.status_code == 204, f"'/specialization/answer' Выполнено 0/1 тестов, ожидается статус 204, получен {response.status_code}"
    
def get_result(token):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(URL + "/specialization/result", headers=headers)
    assert response.status_code == 200, f"'/specialization/result' Выполнено 0/1 тестов, ожидается статус 200, получен {response.status_code}"
    return response.json()