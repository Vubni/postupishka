import requests, os, time
from config import URL


    
if __name__ == "__main__":
    import auth, profile, psychologist, university, schedule, specialization
    
    try:
        token = auth.get_auth_token()
        profile.test_profile_delete_success(token)
    except:
        pass
    # Регистрация и авторизация
    token = auth.run_auth_tests()
    
    # Профиль
    profile.run_all_profile_tests(token)
    
    token = auth.get_auth_token()
    
    psychologist.test_send_question(token)
    psychologist.test_get_dialog(token)
    
    university.run_all_university_tests(token)
    
    schedule.test_add_schedule(token)
    schedule.test_get_schedule(token)
    
    specialization.test_get_question(token)
    specialization.test_send_answer(token)
    specialization.test_get_result(token)
    
    # Очистка
    profile.delete_profile(token)