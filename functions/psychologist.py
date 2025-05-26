from ai.ai import Ai
from ai.prompts import (PROMPT_PSYCHOLOGIST)

ai_psychologist = {}

def create_ai(email:str):
    ai_psychologist[email] = Ai(PROMPT_PSYCHOLOGIST, model="gpt-4.1-mini", max_questions=10)

async def question(email:str, question:str):
    if email not in ai_psychologist:
        create_ai(email)
    return (await ai_psychologist[email].question(question)).answer

async def dialog(email:str):
    if email not in ai_psychologist:
        create_ai(email)
    return ai_psychologist[email].messages[1:]