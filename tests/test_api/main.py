import requests, os, time
from config import URL


    
if __name__ == "__main__":
    
    import profile
    # profile.test_create_user()
    token = profile.test_auth()
    profile.test_profile(token)
    profile.test_tg(token)
    
    import specialization
    number = 5
    while number > 0:
        res = specialization.generate_question(token)
        print(res["question"])
        specialization.answer(token, input())
        number-=1

    res = {"status": "eee"}
    while res["status"] != "done":
        res = specialization.get_result(token)
        print(res)
        time.sleep(1)
    
    # profile.delete_profile(token)