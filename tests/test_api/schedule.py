import requests
from config import URL

def test_add_schedule_success(token):
    """Тест успешного добавления расписания"""
    print("\n=== Тест Sch.1: Успешное добавление расписания ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "content": "Понедельник: 10:00-12:00 Математика, 13:00-15:00 Русский"
    }
    response = requests.post(URL + "/schedule", json=data, headers=headers)
    assert response.status_code == 204, f"Ожидался 204, получен {response.status_code}"
    print("✅ Тест Sch.1 пройден")

def test_add_schedule_invalid_data(token):
    """Тест добавления расписания с некорректными данными"""
    print("\n=== Тест Sch.2: Некорректные данные при добавлении ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Пустой content
    response = requests.post(URL + "/schedule", json={"content": ""}, headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    
    # Отсутствует content
    response = requests.post(URL + "/schedule", json={}, headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    
    # Не JSON
    response = requests.post(URL + "/schedule", data="invalid", headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    print("✅ Тест Sch.2 пройден")

def test_add_schedule_unauthorized():
    """Тест добавления расписания без авторизации"""
    print("\n=== Тест Sch.3: Запрос без авторизации ===")
    headers = {"Authorization": "Bearer invalid_token"}
    data = {
        "content": "Понедельник: 10:00-12:00 Математика"
    }
    response = requests.post(URL + "/schedule", json=data, headers=headers)
    assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
    print("✅ Тест Sch.3 пройден")

def test_get_schedule_success(token):
    """Тест успешного получения расписания"""
    print("\n=== Тест Sch.4: Успешное получение расписания ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/schedule", headers=headers)
    assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "Неверная структура расписания"
    
    if data:
        week = data[0]
        assert "week" in week, "Отсутствует поле 'week'"
        assert "info" in week, "Отсутствует поле 'info'"
        
        for day in week["info"]:
            assert "day" in day, "Отсутствует поле 'day_in_month'"
            assert "schedule" in day, "Отсутствует поле 'schedule'"
            
            for item in day["schedule"]:
                assert "time_start" in item, "Отсутствует поле 'time_start'"
                assert "time_stop" in item, "Отсутствует поле 'time_stop'"
                assert "name" in item, "Отсутствует поле 'name'"
                assert "description" in item, "Отсутствует поле 'description'"
                
    print("✅ Тест Sch.4 пройден")

def test_get_schedule_unauthorized():
    """Тест получения расписания без авторизации"""
    print("\n=== Тест Sch.5: Запрос без авторизации ===")
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(URL + "/schedule", headers=headers)
    assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
    print("✅ Тест Sch.5 пройден")

def test_server_error_handling(token):
    """Тест обработки серверных ошибок"""
    print("\n=== Тест Sch.6: Обработка серверных ошибок ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Добавление слишком большого расписания
    large_content = "A" * 100000
    response = requests.post(URL + "/schedule", json={"content": large_content}, headers=headers)
    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    print("✅ Тест Sch.6 пройден")

def run_all_schedule_tests(token):
    """Запуск всех тестов расписания"""
    print("\n\n=== ТЕСТИРОВАНИЕ РАСПИСАНИЯ ===")
    
    print("\nГруппа 1: Основные сценарии")
    test_add_schedule_success(token)
    test_get_schedule_success(token)
    
    print("\nГруппа 2: Обработка ошибок")
    test_add_schedule_invalid_data(token)
    test_add_schedule_unauthorized()
    test_get_schedule_unauthorized()
    test_server_error_handling(token)
    
    print("\n✅ ВСЕ ТЕСТЫ РАСПИСАНИЯ ПРОЙДЕНЫ")