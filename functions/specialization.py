from ai.ai import Ai
from ai.prompts import (PROMPT_QUESTIONS, PROMPT_SHORTLIST, 
                        PROMPT_INITIAL_QUERIES, PROMPT_SHORTENER, 
                        PROMPT_UNIFIER, PROMPT_REFINE_QUERIES,
                        PROMPT_FINAL_OUTPUT)
import googlesearch as gs
import requests
from bs4 import BeautifulSoup
import json, asyncio
from functions import auth as func_db
from datetime import datetime
from database.database import Database

def current_study_year():
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    if current_month >= 9:
        academic_year = f"{current_year}/{current_year + 1}"
    else:
        academic_year = f"{current_year - 1}/{current_year}"
    return academic_year

list_ai = {}
shortener_ai = Ai(PROMPT_SHORTENER, model="gpt-4.1-nano")
unifier_ai = Ai(PROMPT_UNIFIER, model="gpt-4.1-mini")
get_result_wait = {}

async def check_browse(content:str):
    try:
        results=gs.search(content,num_results=4)
    except:
        try:
            results=gs.search(content,num_results=4)
        except:
            return ""
    result_text = ""
    for link in results:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = (' '.join(soup.get_text().split()))[:200000]
                status = False
                while not status:
                    try:
                        result_text += (await shortener_ai.question(f"Изначально искали: {content}\nТребуется сократить:" + text, False)).answer + "\n\n"
                        status = True
                    except:
                        await asyncio.sleep(5)
        except:
            continue
    return (await unifier_ai.question(result_text[:400000], False)).answer

async def create_ai(email:str):
    list_ai[email] = Ai(PROMPT_QUESTIONS)
    subjects = await func_db.get_subjects(email)
    profile = await func_db.profile_get(email)
    content = f"Текущий учебный год: {current_study_year()}\n"
    content += "Класс абитуриента: " + str(profile["class_number"]) + "\nпредметы, которые сдаёт:"
    for subject in subjects:
        content+= "\n" + subject["subject"] + " | Баллы сейчас: " + str(subject["current_score"]) + " | Рассчитывает на: " + str(subject["desired_score"])
    list_ai[email].add_question(content)

async def generate_question(email:str):
    if email not in list_ai:
        await create_ai(email)
    if list_ai[email].messages[-1]["role"] == "system":
        return json.loads(list_ai[email].messages[-1]["content"])
    return json.loads((await list_ai[email].question()).answer)

def add_answer(email:str, content:str):
    if email not in list_ai:
        return False
    if list_ai[email].messages[-1]["role"] == "user":
        return False
    list_ai[email].add_question(content)
    return True

async def get_result_handler(email:str):
    if email not in get_result_wait:
        get_result_wait[email] = asyncio.create_task(get_result(email))
        return {"status": "processing"}
    if get_result_wait[email].done():
        res = {"status": "done", "result": get_result_wait[email].result()}
        del get_result_wait[email]
        return res
    else:
        return {"status": "processing"}

async def get_result(email:str):
    if email not in list_ai:
        return False
    list_ai[email].edit_system_prompt(PROMPT_INITIAL_QUERIES)
    tasks = []
    questons = (await list_ai[email].question("Создай 3 запроса для браузера", False)).answer.split("$")
    for queston in questons:
        tasks.append(check_browse(queston))
    result = await asyncio.gather(*tasks)
    for res in result:
        list_ai[email].add_question("Данные из интернета о вузах: " + res)
    
    list_ai[email].edit_system_prompt(PROMPT_SHORTLIST)
    res = await list_ai[email].question("Выдай список вузов")

    list_ai[email].edit_system_prompt(PROMPT_REFINE_QUERIES)
    tasks = []
    questons = (await list_ai[email].question("Создай до 6 запросов для браузера по вузам, которые ты получил до этого", False)).answer.split("$")
    for queston in questons:
        tasks.append(check_browse(queston))
    result = await asyncio.gather(*tasks)
    for res in result:
        list_ai[email].add_question("Данные из интернета о вузах: " + res)

    list_ai[email].edit_system_prompt(PROMPT_FINAL_OUTPUT)
    res = await list_ai[email].question("Выдай список вузов")
    del list_ai[email]
    return json.loads(res.answer)

async def get_time(email):
    async with Database() as db:
        res = await db.execute("SELECT date_time FROM specializations WHERE email=$1", (email,))
    if not res:
        return False
    return res["date_time"]