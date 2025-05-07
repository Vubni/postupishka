import time
from openai import OpenAI
from config import API_KEY, PROXY_USER, PROXY_PASS, PROXY_IP, PROXY_PORT

import httpx
from httpx import HTTPTransport

proxy_url = "socks5h://PzHdk8fT:9S8e4TCM@45.130.184.97:62845"

transport = HTTPTransport(proxy=httpx.Proxy(proxy_url))

client = OpenAI(
    api_key=API_KEY,
    http_client=httpx.Client(
        transport=transport,
        timeout=httpx.Timeout(30)
    )
)

def calculate_cost(prompt_tokens, completion_tokens):
    INPUT_COST_PER_TOKEN = 0.005 / 1000  # $5 за 1 млн входных токенов
    OUTPUT_COST_PER_TOKEN = 0.015 / 1000  # $15 за 1 млн выходных токенов
    return (prompt_tokens * INPUT_COST_PER_TOKEN) + (completion_tokens * OUTPUT_COST_PER_TOKEN)

class Answer_ai:
    def __init__(self, messages=None, answer="", price=0.0, generation_time=0.0):
        self.messages = messages if messages is not None else []
        self.answer = answer
        self.price = price
        self.generation_time = generation_time

class Ai:
    def __init__(self, system_prompt=None, model="gpt-4.1"):
        self.model = model
        self.messages = []
        self.system_prompt = system_prompt
        self.price = 0
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
            
    def add_question(self, content:str):
        self.messages.append({"role": "user", "content": content})
    
    def question(self, content=None, memory=False):
        if content:
            user_message = {"role": "user", "content": content}
        
            # Подготовка сообщений для запроса
            if memory:
                self.messages.append(user_message)
                current_messages = self.messages
            else:
                if self.system_prompt:
                    current_messages = [{"role": "system", "content": self.system_prompt}, user_message]
                else:
                    current_messages = [user_message]
        else:
            current_messages = self.messages
        
        # Отправка запроса в OpenAI
        start_time = time.time()
        response = client.chat.completions.create(
            model=self.model,
            messages=current_messages,
            temperature=0.7
        )
        end_time = time.time()
        
        # Обработка ответа
        answer_content = response.choices[0].message.content
        usage = response.usage
        cost = calculate_cost(usage.prompt_tokens, usage.completion_tokens)
        generation_time = end_time - start_time
        
        # Формирование истории сообщений для ответа
        if memory:
            self.messages.append({"role": "assistant", "content": answer_content})
            answer_messages = self.messages.copy()
        else:
            answer_messages = current_messages.copy()
            answer_messages.append({"role": "assistant", "content": answer_content})
        
        self.price += cost
        # Создание объекта ответа
        return Answer_ai(
            messages=answer_messages,
            answer=answer_content,
            price=cost,
            generation_time=generation_time
        )
        
    def clear_messages(self):
        self.messages = []
        return True

def main():
    ai = Ai(system_prompt="Ты школьный преподаватель", model="gpt-4.1")

    # Первый вопрос с сохранением в памяти
    response1 = ai.question("Как составить расписание?", memory=True)
    print(response1.answer)
    print(f"Стоимость: ${response1.price:.4f}")

    # Второй вопрос с использованием памяти
    response2 = ai.question("Добавь перерывы на обед", memory=True)
    print(response2.answer)

    # Независимый запрос без использования памяти
    response3 = ai.question("Сколько длится урок?", memory=False)
    print(response3.answer)
#     messages = [
#         {"role": "system", "content": """Представь, что ты школьный преподаватель. Твоя задача — составить расписание с учётом:

# Дней недели (Пн, Вт, Ср, Чт, Пт, Сб, Вс).
# Времени окончания школы (уточню позже).
# Времени на дорогу домой (уточню позже).
# Времени отбоя (уточню позже).
# Количества часов на подготовку к экзаменам в неделю (уточню позже).
# Расписание должно быть в формате JSON:
# {
#   "расписание": [
#     {
#       "день": "Пн",
#       "время_начала": "HH:MM",
#       "время_окончания": "HH:MM",
#       "тип": "школа/подготовка/перерыв",
#       "предмет": "название (только для школы)"
#     },
#     ...
#   ]
# }
# Условия:

# После окончания школы и дороги домой начинай подготовку.
# Учти время отбоя (заканчивай все занятия до него).
# Распредели часы подготовки равномерно по дням.
# Укажи перерывы на обед/отдых (минимум 30 минут).
# Для школьных уроков укажи название предмета, для подготовки — "экзамен".
# Выведи только JSON, без текста."""},
#         {"role": "user", "content": "Я хочу заниматься математикой 3 часа в неделю, 7 часов русским, 4 информатикой. Я заканчиваю обучение в школе в 15:00, еду домой час. Я ложусь в 12 ночи."}
#     ]

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4.1",
#             messages=messages,
#             temperature=0.7
#         )
        
#         # Получаем данные об использовании [[1]][[9]]
#         usage = response.usage
#         prompt_tokens = usage.prompt_tokens
#         completion_tokens = usage.completion_tokens
#         total_cost = calculate_cost(prompt_tokens, completion_tokens)
        
#         print("Расписание:")
#         print(response.choices[0].message.content.strip())
#         print(f"\nТокены: вход - {prompt_tokens}, выход - {completion_tokens}")
#         print(f"Стоимость запроса: ${total_cost:.4f}")

#     except Exception as e:
#         print(f"Ошибка: {str(e)}")

if __name__ == "__main__":
    main()