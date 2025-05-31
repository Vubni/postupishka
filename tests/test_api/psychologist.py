import requests
from config import URL

def test_send_question_success(token):
    """Тест успешной отправки вопроса"""
    print("\n=== Тест P.1: Успешная отправка вопроса ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"question": "Как справиться со стрессом?"}
    response = requests.post(URL + "/psychologist", json=data, headers=headers)
    
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    
    data = response.json()
    assert "answer" in data, "Ответ от психолога отсутствует"
    assert isinstance(data["answer"], str), "Неверный формат ответа"
    
    print(f"  Ответ психолога: {data['answer'][:50]}...")
    print("✅ Тест P.1 пройден")

def test_send_question_invalid_format(token):
    """Тест отправки некорректного формата вопроса"""
    print("\n=== Тест P.2: Некорректный формат вопроса ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Без обязательного поля question
    response = requests.post(URL + "/psychologist", json={}, headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    
    # Не JSON
    response = requests.post(URL + "/psychologist", data="invalid", headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    print("✅ Тест P.2 пройден")

def test_send_question_empty(token):
    """Тест отправки пустого вопроса"""
    print("\n=== Тест P.3: Отправка пустого вопроса ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"question": ""}
    response = requests.post(URL + "/psychologist", json=data, headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    print("✅ Тест P.3 пройден")

def test_get_dialog_success(token):
    """Тест успешного получения диалога"""
    print("\n=== Тест P.4: Успешное получение диалога ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/psychologist", headers=headers)
    
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    dialog = response.json()
    
    assert isinstance(dialog, list), "Ожидался массив сообщений"
    assert len(dialog) > 0, "Диалог пуст"
    
    for message in dialog:
        assert "content" in message, "Отсутствует поле 'content'"
        assert "role" in message, "Отсутствует поле 'role'"
        assert message["role"] in ["user", "assistant"], "Неверная роль"
        
    print(f"  Получено сообщений: {len(dialog)}")
    print("✅ Тест P.4 пройден")

def test_get_dialog_unauthorized():
    """Тест запроса диалога без авторизации"""
    print("\n=== Тест P.5: Запрос диалога без авторизации ===")
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(URL + "/psychologist", headers=headers)
    assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
    print("✅ Тест P.5 пройден")

def test_dialog_pagination(token):
    """Тест пагинации диалога"""
    print("\n=== Тест P.6: Проверка ограничения количества сообщений ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/psychologist", headers=headers)
    
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    dialog = response.json()
    
    assert len(dialog) <= 20, "Превышено максимальное количество сообщений"
    print(f"  Количество сообщений: {len(dialog)} (максимум 10)")
    print("✅ Тест P.6 пройден")

def test_question_response_time(token):
    """Тест времени ответа на вопрос"""
    print("\n=== Тест P.7: Время ответа на вопрос ===")
    import time
    headers = {"Authorization": f"Bearer {token}"}
    data = {"question": "Как улучшить концентрацию?"}
    
    start_time = time.time()
    response = requests.post(URL + "/psychologist", json=data, headers=headers)
    elapsed_time = time.time() - start_time
    
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    assert elapsed_time < 7, f"Время ответа слишком велико: {elapsed_time:.2f} секунд"
    
    print(f"  Время ответа: {elapsed_time:.2f} секунд")
    print("✅ Тест P.7 пройден")

def run_all_psychologist_tests(token):
    """Запуск всех тестов психолога"""
    print("\n\n=== ТЕСТИРОВАНИЕ ПСИХОЛОГА ===")
    
    print("\nГруппа 1: Основные сценарии")
    test_send_question_success(token)
    test_get_dialog_success(token)
    
    print("\nГруппа 2: Обработка ошибок")
    test_send_question_invalid_format(token)
    test_send_question_empty(token)
    test_get_dialog_unauthorized()
    
    print("\nГруппа 3: Дополнительные проверки")
    test_dialog_pagination(token)
    test_question_response_time(token)
    
    print("\n✅ ВСЕ ТЕСТЫ ПСИХОЛОГА ПРОЙДЕНЫ")