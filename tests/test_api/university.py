import requests
from config import URL

def test_add_university_success(token):
    """Тест успешного добавления университета"""
    print("=== Тест 1.1: Добавление университета с корректными данными ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "university": "МГУ",
        "direction": "Информатика",
        "scores": {"min": 200, "avg": 250, "bud": 280}
    }
    response = requests.post(URL + "/university/add", json=data, headers=headers)
    assert response.status_code == 204, f"Ожидался статус 204, получен {response.status_code}"
    print("✅ Тест 1.1 пройден успешно")

def test_add_university_without_direction(token):
    """Тест добавления университета без указания направления"""
    print("=== Тест 1.2: Добавление университета без направления ===")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "university": "СПбГУ",
        "scores": {"min": 180, "avg": 220, "bud": 260}
    }
    response = requests.post(URL + "/university/add", json=data, headers=headers)
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
    print("✅ Тест 1.2 пройден успешно")

def test_add_university_missing_required_fields(token):
    """Тест попытки добавления без обязательных полей"""
    print("=== Тест 1.3: Проверка обязательных полей ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {"university": "МФТИ"}
    response = requests.post(URL + "/university/add", json=data, headers=headers)
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
    
    data = {"scores": {"min": 200, "avg": 250, "bud": 280}}
    response = requests.post(URL + "/university/add", json=data, headers=headers)
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
    print("✅ Тест 1.3 пройден успешно")

def test_add_university_invalid_score_values(token):
    """Тест добавления с некорректными значениями в scores"""
    print("=== Тест 1.4: Некорректные значения в scores ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {
        "university": "ВШЭ",
        "scores": {"min": "200", "avg": 250, "bud": 280}
    }
    response = requests.post(URL + "/university/add", json=data, headers=headers)
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
    
    data = {
        "university": "ИТМО",
        "scores": {"min": -50, "avg": 250, "bud": 280}
    }
    response = requests.post(URL + "/university/add", json=data, headers=headers)
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
    print("✅ Тест 1.4 пройден успешно")

def test_add_university_invalid_json(token):
    """Тест добавления с невалидным JSON"""
    print("=== Тест 1.5: Невалидный JSON ===")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    invalid_json = '{"university": "МГТУ", "scores": {"min": 200, "avg": 250, "bud": 280}'
    response = requests.post(URL + "/university/add", data=invalid_json, headers=headers)
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
    print("✅ Тест 1.5 пройден успешно")

def test_add_university_unauthorized():
    """Тест добавления без авторизации"""
    print("=== Тест 1.6: Попытка добавления без токена ===")
    data = {
        "university": "НИУ",
        "direction": "НИУ",
        "scores": {"min": 200, "avg": 250, "bud": 280}
    }
    response = requests.post(URL + "/university/add", json=data)
    assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
    print("✅ Тест 1.6 пройден успешно")

def test_get_universities_structure(token):
    """Тест структуры ответа GET /university"""
    print("=== Тест 2.1: Проверка структуры ответа ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(URL + "/university", headers=headers)
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    
    universities = response.json()
    if universities:
        uni = universities[0]
        assert "university" in uni, "Отсутствует поле 'university'"
        assert "direction" in uni, "Отсутствует поле 'direction'"
        assert "scores" in uni, "Отсутствует поле 'scores'"
        assert isinstance(uni['scores'], dict), "Неверный формат поля 'scores'"
        assert 'min' in uni['scores'], "Отсутствует 'min' в scores"
        assert 'avg' in uni['scores'], "Отсутствует 'avg' в scores"
        assert 'bud' in uni['scores'], "Отсутствует 'bud' в scores"
    print("✅ Тест 2.1 пройден успешно")

def test_university_crud_flow(token):
    """Тест полного цикла CRUD для университетов"""
    print("=== Тест 2.2: Проверка CRUD операций ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Добавление университета
    add_data = {
        "university": "Тестовый Университет",
        "direction": "Тестовое направление",
        "scores": {"min": 150, "avg": 200, "bud": 250}
    }
    response = requests.post(URL + "/university/add", json=add_data, headers=headers)
    assert response.status_code == 204, "Ошибка при добавлении университета"
    
    # Получение списка университетов
    response = requests.get(URL + "/university", headers=headers)
    assert response.status_code == 200, "Ошибка при получении списка"
    universities = response.json()
    found = any(uni['university'] == "Тестовый Университет" for uni in universities)
    assert found, "Добавленный университет не найден в списке"
    
    print("✅ Тест 2.2 пройден успешно")

def run_all_university_tests(token):
    """Запуск всех тестов для университетов"""
    print("=== ТЕСТИРОВАНИЕ ЭНДПОИНТОВ УНИВЕРСИТЕТОВ ===\n")
    
    print("Группа 1: Тесты добавления университетов")
    test_add_university_success(token)
    test_add_university_without_direction(token)
    test_add_university_missing_required_fields(token)
    test_add_university_invalid_score_values(token)
    test_add_university_invalid_json(token)
    test_add_university_unauthorized()
    
    print("\nГруппа 2: Тесты получения университетов")
    test_get_universities_structure(token)
    test_university_crud_flow(token)
    
    print("\n✅ ВСЕ ТЕСТЫ ДЛЯ УНИВЕРСИТЕТОВ ПРОЙДЕНЫ УСПЕШНО")