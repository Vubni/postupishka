from database.database import Database
import json
from ai.ai import Ai
from ai.prompts import (PROMPT_SCHEDULE_ANALIZE, PROMPT_SCHEDULE_CREATE)
from datetime import datetime, timedelta
import re

def is_safe_sql_query(query: str) -> bool:
    """
    Проверяет, является ли SQL-запрос безопасным.
    Разрешены только операции INSERT, UPDATE и DELETE для таблицы 'schedule'.
    Запрещены любые другие операции и манипуляции с другими таблицами или объектами БД.

    :param query: SQL-запрос в виде строки
    :return: True, если запрос безопасен, иначе False
    """
    query = query.strip().lower()

    allowed_operations = r"^(insert into schedule|update schedule|delete from schedule)"

    if not re.match(allowed_operations, query):
        return False

    forbidden_patterns = [
        r"(;)",  # Запрещаем множественные запросы через точку с запятой
        r"(drop|truncate|alter|create|grant|revoke)",  # Запрещаем DDL-операции
        r"(insert into\s+\w+\s+select)"  # Запрещаем INSERT с SELECT
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, query):
            return False

    if "schedule" not in query:
        return False

    return True

def get_first_day_of_week(week_offset=0):
    today = datetime.today().date()
    monday = today - timedelta(days=today.weekday())
    first_day = monday + timedelta(weeks=week_offset)
    
    return first_day.day



async def add_info(email:str, content:str):
    ai_analyzer = Ai(PROMPT_SCHEDULE_ANALIZE, model="gpt-4.1")
    ai_create = Ai(PROMPT_SCHEDULE_CREATE, model="gpt-4.1")
    async with Database() as db:
        await db.execute("DELETE FROM schedule WHERE week=$1", (get_first_day_of_week(-1),))
        info = json.dumps(await db.execute_all("SELECT * FROM schedule WHERE email=$1", (email,)))
        ai_analyzer.add_question(info)
        ai_create.add_question(info)
        
        res = await ai_analyzer.question("Хочу добавить к расписанию: " + content)
        if res.answer.lower() != "true":
            return {"status": False, "text": res.answer}
        result = (await ai_create.question(f"Почта: {email}, начало недели текущей: {get_first_day_of_week()}, начало недели следующей: {get_first_day_of_week(1)}. Что хочет человек: " + content)).answer.split("$")
        for res in result:
            if not is_safe_sql_query(res):
                continue
            try:
                await db.execute(res)
            except:
                pass
    return {"status": True}

async def get_info(email:str):
    async with Database() as db:
        await db.execute("DELETE FROM schedule WHERE week=$1", (get_first_day_of_week(-1),))
        result = await db.execute_all("SELECT week, day, schedule FROM schedule WHERE email=$1", (email,))
    if not result:
        return []
    result = list(result)
    main_result = []
    for res in result:
        stats = False
        for item in main_result:
            if res["week"] == item["week"]:
                stats = True
                item["info"].append({"day": res["day"], "schedule": list(json.loads(res["schedule"]))})
        if not stats:
            main_result.append({"week": res["week"], "info": [{"day": res["day"], "schedule": list(json.loads(res["schedule"]))}]})
    return main_result