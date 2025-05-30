import requests
from config import URL

def test_get_question_success(token):
    """Тест успешного получения вопроса"""
    print("\n=== Тест S.1: Успешное получение вопроса ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/specialization/question", headers=headers)
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    
    data = response.json()
    assert "question" in data, "Отсутствует поле 'question'"
    assert "counts_remaind" in data, "Отсутствует поле 'counts_remaind'"
    assert isinstance(data["question"], str), "Неверный формат вопроса"
    assert isinstance(data["counts_remaind"], int), "Неверный формат счетчика"
    
    print(f"  Вопрос: {data['question']}")
    print(f"  Осталось вопросов: {data['counts_remaind']}")
    print("✅ Тест S.1 пройден")

def test_get_question_unauthorized():
    """Тест запроса без авторизации"""
    print("\n=== Тест S.2: Запрос без авторизации ===")
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(URL + "/specialization/question", headers=headers)
    assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
    print("✅ Тест S.2 пройден")

def test_send_answer_success(token):
    """Тест успешной отправки ответа"""
    print("\n=== Тест S.3: Успешная отправка ответа ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"answer": "Тестовый ответ"}
    response = requests.post(URL + "/specialization/answer", json=data, headers=headers)
    assert response.status_code == 204, f"Ожидался 204, получен {response.status_code}"
    print("✅ Тест S.3 пройден")

def test_send_answer_invalid_format(token):
    """Тест отправки некорректного формата ответа"""
    print("\n=== Тест S.4: Некорректный формат ответа ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Без обязательного поля answer
    response = requests.post(URL + "/specialization/answer", json={}, headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    
    # Не JSON
    response = requests.post(URL + "/specialization/answer", data="invalid", headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    print("✅ Тест S.4 пройден")

def test_specialization_timer(token):
    """Тест таймера специализации"""
    print("\n=== Тест S.5: Проверка таймера ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/specialization", headers=headers)
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    
    data = response.json()
    assert "days" in data and "hours" in data and "minutes" in data
    print(f"  Осталось времени: {data['days']}д {data['hours']}ч {data['minutes']}м")
    print("✅ Тест S.5 пройден")

def test_get_result_minimal(token):
    """Минимальный тест получения результата"""
    print("\n=== Тест S.6: Получение результата ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/specialization/result", headers=headers)
    assert response.status_code in (200, 202), f"Непредвиденный статус: {response.status_code}"
    
    if response.status_code == 200:
        data = response.json()
        assert "status" in data and "result" in data
        print(f"  Статус: {data['status']}")
    else:
        print("  Результат еще не готов (статус 202)")
    print("✅ Тест S.6 пройден")

def run_all_specialization_tests(token):
    """Запуск всех тестов специализации"""
    print("\n\n=== ТЕСТИРОВАНИЕ СПЕЦИАЛИЗАЦИИ ===")
    
    print("\nГруппа 1: Основные сценарии")
    test_get_question_success(token)
    test_send_answer_success(token)
    test_specialization_timer(token)
    test_get_result_minimal(token)
    
    print("\nГруппа 2: Обработка ошибок")
    test_get_question_unauthorized()
    test_send_answer_invalid_format(token)
    
    print("\n✅ ВСЕ ТЕСТЫ СПЕЦИАЛИЗАЦИИ ПРОЙДЕНЫ")