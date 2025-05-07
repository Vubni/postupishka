from ai.yandex_ai import Analyzer
from datetime import datetime
from telegram.create_bot import bot

notification_ai = Analyzer("""Создай дружеское напоминание о предстоящем занятии/деле в формате:
— «Через [время] — [предмет/дело]! Не забудь [предметы/рекомендации] [эмодзи]. Ничего лишнего не пиши""")

async def send_notification(user_id, lesson, time_difference):
    answer = notification_ai.question(f"Занятие {lesson} начнётся в {time_difference}")
    await bot.send_message(user_id, answer)

async def analyz_notification():
    #.... АНАЛИЗ ПОСТОЯННЫЙ, ПОКА НЕ БУДЕТ СОБЫТИЕ ЧЕРЕЗ 30 МИНУТ
    await send_notification(None, None, None)