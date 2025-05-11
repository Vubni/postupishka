from ai.ai import Ai
from ai.prompts import PROMPT_QUESTIONS, PROMPT_SPECIALISATION, PROMPT_BROWSE, PROMPT_ABBREVIATIONS
import googlesearch as gs
import requests
from bs4 import BeautifulSoup
import json, asyncio
from database import functions as func_db

list_ai = {}
browse_ai = Ai(PROMPT_ABBREVIATIONS, model="gpt-4.1-nano")
get_result_wait = {}

async def check_browse(content:str):
    results=gs.search(content,num_results=2)
    result_text = ""
    for link in results:
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            result_text += ' '.join(soup.get_text().split())
    res = await browse_ai.question(f"Изначально искали: {content}\n"  + result_text)
    return res.answer

async def create_ai(email:str):
    list_ai[email] = Ai(PROMPT_QUESTIONS)
    subjects = await func_db.get_subjects(email)
    profile = await func_db.profile_get(email)
    content = "Класс абитуриента: " + str(profile["class"]) + "\nпредметы, которые сдаёт:"
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
        print(list_ai[email].messages)
        print(list_ai[email].messages[-1])
        return False
    list_ai[email].add_question(content)
    return True

async def get_result_handler(email:str):
    if email not in get_result_wait:
        get_result_wait[email] = asyncio.create_task(get_result(email))
        return {"status": "processing"}
    if get_result_wait[email].done():
        return {"status": "done", "result": get_result_wait[email].result()}
    else:
        return {"status": "processing"}

async def get_result(email:str):
    if email not in list_ai:
        return False
    list_ai[email].edit_system_prompt(PROMPT_BROWSE)
    for i in range(5):
        res = await check_browse((await list_ai[email].question("Создай запрос для браузера")).answer)
        list_ai[email].add_question("Данные из интернета о вузах: " + res)

    
    list_ai[email].edit_system_prompt(PROMPT_SPECIALISATION)
    res = await list_ai[email].question("Выдай список вузов")
    del list_ai[email]
    return json.loads(res.answer)