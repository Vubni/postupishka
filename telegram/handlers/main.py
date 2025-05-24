from json import load, dumps
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from html import escape
from telegram.FSM import fsm
from aiogram.fsm.context import FSMContext
from aiogram import types
from telegram import botstates
from telegram.create_bot import bot
from ai.yandex_ai import Psychologist, Analyzer
from functions import auth as func_db
from telegram.keyboards import main as kb

psycho_ai = {}
ai = {}
ask_answers = {}
async def create_physicol(user_id):
    global psycho_ai
    if user_id in psycho_ai:
        psycho_ai[user_id].clear()
        return
    psycho_ai[user_id] = Psychologist()
    psycho_ai[user_id] = await psycho_ai[user_id].init()

async def create_ai(user_id):
    global ai
    if user_id in ai:
        ai[user_id].clear()
        return
    ai[user_id] = await Analyzer().init("""Ты — виртуальный консультант по поступлению в вуз. Задавай вопросы по одному, чтобы помочь пользователю определиться с выбором. Следуй схеме:

Профессиональные интересы: «Какую сферу деятельности вы рассматриваете? Например, IT, медицина, инженерия» 
Баллы ЕГЭ: «Какие экзамены вы сдаёте и какой примерный балл ожидаете?» 
Локация: «В каком городе/регионе хотите учиться?»
Бюджет/платное: «Вас интересуют бюджетные места или готовы рассмотреть платное обучение?»
Дополнительно: «Важны ли стипендии, практики»""", memory=True)


TRANS = {
    "russian": "Русский язык",
    "literature": "Литература",
    "profmat": "Математика проф.",
    "basemat": "Математика база",
    "chem": "Химия",
    "geo": "География",
    "obsh": "Обществознание",
    "inf": "Информатика",
    "history": "История",
    "phys": "Физика",
    "bio": "Биология",
    "foreign": "Иностранный язык"
}

router = Router()

@router.message(CommandStart())
async def send_welcome(message: types.Message, state: FSMContext):
    if not await func_db.check_connect(message.from_user.id):
        return await message.answer("Чтобы начать использовать бота - привяжите профиль в <a href='https://online-postupishka.ru/profile/'>личном кабинете</a>")
        
    await message.answer("""🎓 Ваш персональный помощник в мире образования

Telegram-бот  "Онлайн Поступишка" создан специально для тех, кто стоит перед важным выбором – поступление в университет. Мы понимаем, что этот процесс может быть пугающим и запутанным, поэтому разработали уникального помощника!\n\nНаш сайт - http://online-postupishka.netlify.app""", reply_markup=kb.main_menu_keyboard)
    return await state.set_state(botstates.MainMenuStates.main)

    
@router.callback_query(botstates.RegistrationStates.waiting_for_subjects)
async def process_subjects(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    data_got = await state.get_data()
    data_got["userid"] = callback_query.from_user.id
    if "subjects" not in data_got:
        data_got["subjects"] = []
    if data != "done":
        if data in data_got["subjects"]:
            data_got["subjects"].remove(data)
            await callback_query.answer(f"Вы отменили выбор: {TRANS[data]}")
        else:
            data_got["subjects"].append(data)
            await callback_query.answer(f"Вы выбрали: {TRANS[data]}")
        if data in ["profmat", "basemat"]:
            if data == "profmat" and "basemat" in data_got["subjects"]:
                data_got["subjects"].remove("basemat")
            elif data == "basemat" and "profmat" in data_got["subjects"]:
                data_got["subjects"].remove("profmat")
        await callback_query.message.edit_text("Привет! Я — твой помощник в выборе вуза и подготовке к экзаменам. Давай начнём с короткой анкеты, чтобы я понял, как тебе помочь! 🎓\n\n Какие предметы ты сдаёшь? Когда выберешь, нажми 'Я выбрал'", reply_markup=kb.create_subjects(data_got["subjects"]))
    await state.update_data(data_got)
    if data=="done":
        functions.register_subjects(data_got["userid"], data_got["subjects"])
        await callback_query.message.answer(f"Молодец! Пора приступать к подготовке", reply_markup=kb.main_menu_keyboard)
        await state.set_state(botstates.MainMenuStates.main)
        await callback_query.message.delete()

@router.message(lambda message: message.text in ["Помощь с расписанием🔒", "Помощь с составлением расписания🔒"])
async def main_menu(message: types.Message, state: FSMContext):
    await message.answer("Функция в разработке. . .")

@router.message(lambda message: message.text.lower() in ["психолог👩🏻‍⚕️", "аккаунт💳", "помощь с выбором специальности✅", "тренажёры🚀", "помощь с расписанием📅"])
async def main_menu(message: types.Message, state: FSMContext):
    if message.text.lower() == "психолог👩🏻‍⚕️":
        msg = await message.answer("Создание модели...")
        await create_physicol(message.from_user.id)
        await msg.edit_text("Опиши свою проблему и ИИ-ассистент окажет тебе моральную поддержку. Чтобы завершить сеанс психотерапии, напиши /stop")
        await state.set_state(botstates.MainMenuStates.psycho)

    if message.text.lower() == "тренажёры🚀":
        await message.answer("🚀Выберите тренажёр из представленных", reply_markup=kb.tests_keyboard)
        await state.set_state(botstates.MainMenuStates.tests)

    if message.text.lower() == "помощь с выбором специальности✅":
        await message.answer("""🌟 <b>Приветствуем в подборе специальности!</b> 🌟

Чтобы мы могли подобрать для тебя идеальный вариант, нужно ответить на <b>7 простых вопросов</b>. 

🚀 <b>Как это работает?</b>
1. Отвечай на вопросы максимально честно
2. Не задерживайся слишком долго над ответами
3. Используй кнопки или текстовые ответы

⚠️ <b>Хочешь прервать тест?</b>
- Напиши "Стоп" для полного завершения
- Или "Завершить" для моментального анализа

Все данные обрабатываются анонимно и не сохраняются ✅

Готов начать? Тогда поехали! 🚀""")
        msg = await message.answer("Создание модели. . .")
        await create_ai(message.from_user.id)
        await msg.edit_text("Подбор вопроса. . .")
        try:
            await msg.edit_text(await ai[message.from_user.id].question(f"Человек ответил: {message.text}\nЗадай вопрос ему по инструкции"))
        except Exception as e:
            print(e)
            await msg.edit_text("При генерации вопроса произошла ошибка на стороне YandexGPT")
        await state.set_state(botstates.Choice.q)
    if message.text == "Аккаунт💳":
        subjects_mass = functions.get_subjects(message.from_user.id)
        subjects = ""
        for item in subjects_mass:
            subjects += TRANS[item["subject"]] + ", "
        subjects = subjects[:-2]
        await message.answer(f"""
        🆔Ваш id telegram: {message.from_user.id}
⭐️Информация о подписке:
 ├ Тип: Pro
 ├ Подписка оформлена: 19.04.2025
 ├ Действует до: 20.04.2025
 ├ Куплена по цене: 0⭐️/месяц
 └ Акция: Применялась

Выбранные вами предметы: {subjects}
        """, reply_markup=kb.profile)

    if message.text in ["Тренажёры🔒", "Помощь с составлением расписания🔒", "Помощь с расписанием🔒"]:
        await message.answer("Ещё в разработке✅")

    if message.text == "Помощь с расписанием📅":
        await message.answer("""
Расскажи, во сколько в среднем ты тратишь времени на поездку от школы до дома, во сколько хочешь ложиться спать и сколько времени ты хочешь тратить на каждый предмет в неделю.")

Пример:
Я хочу заниматься математикой 3 часа в неделю, 7 часов русским, 4 информатикой. Я заканчиваю обучение в школе в 15:00, еду домой час. Я ложусь в 12 ночи.

""")
        await state.set_state(botstates.MainMenuStates.daily_help)

@router.message(botstates.MainMenuStates.daily_help)
async def get_daily_help(message: types.Message, state: FSMContext):
    await state.set_state(botstates.Wait.wait_generation)
    await message.answer("Подожди ответа ИИ")
    aiDaily = await Analyzer().init("Представь, что ты школьный преподаватель и должен составить мне расписание обучения. Я учусь в школе до определённого времени каждый день, но мне надо готовиться к экзаменами. Я укажу сколько часов мне на это требуется за неделю. Твоя задача распределить. Также я ложусь в определённое время и трачу определённое время на дорогу домой. ",base=False)
    answer = await aiDaily.question(message.text)
    await message.answer(answer)
    await message.answer("Возвращаю вас в главное меню✅")
    await state.set_state(botstates.MainMenuStates.main)
    

@router.message(botstates.Wait.wait_generation) 
async def choice1(message: types.Message, state: FSMContext):
    return await message.answer("Ожидайте завершения генерации ответа")


@router.message(botstates.Choice.q)  # Используем message вместо callback_query
async def choice1(message: types.Message, state: FSMContext):
    if message.text.lower() == "стоп":
        await state.set_state(botstates.MainMenuStates.main)
        return await message.answer("Обработка остановлена!")
    if message.text.lower() == "завершить":
        return await askainow(message, state)
    await state.set_state(botstates.Wait.wait_generation)
    msg = await message.answer("Подбор вопроса. . .")
    try:
        await msg.edit_text(await ai[message.from_user.id].question(f"Человек ответил: {message.text}\nЗадай вопрос ему по инструкции"))
    except Exception as e:
        print(e)
        await msg.edit_text("При генерации вопроса произошла ошибка на стороне YandexGPT")
    await state.set_state(botstates.Choice.q)
    if ai[message.from_user.id].message_count >= 6:
        await state.set_state(botstates.Choice.AskAI)


@router.message(botstates.Choice.AskAI)
async def askainow(message: types.Message, state:FSMContext):
    await state.set_state(botstates.MainMenuStates.main)
    msg = await message.answer("Анализ ответов...")
    subjects_mass = functions.get_subjects(message.from_user.id)
    subjects = ""
    for item in subjects_mass:
        subjects += TRANS[item["subject"]] + ", "
    subjects = subjects[:-2]
    answer = await ai[message.from_user.id].question(f"Человек ответил: {message.text}. Также информация о предметах человека: {subjects}. Всё, выдай результат, какие вузы подходят.",
                               "llama")
    await msg.edit_text(answer)
    await message.answer("Если у тебя будет вопросы по этой теме, задай их психологу", reply_markup=kb.main_menu_keyboard)


@router.message(botstates.MainMenuStates.psycho)  # Используем message вместо callback_query
async def psycho(message: types.Message, state: FSMContext):
    if message.text == "/stop":
        await message.answer("Сеанс закончен", reply_markup=kb.main_menu_keyboard)
        await state.set_state(botstates.MainMenuStates.main)
    else:
        await state.set_state(botstates.Wait.wait_generation)
        msg = await message.answer("Обдумываю ваш запрос. . .")
        try:
            await msg.edit_text(await psycho_ai[message.from_user.id].user_ask(message.text))
        except:
            await message.answer("Ваш запрос не прошёл цензуру, простите")
        await state.set_state(botstates.MainMenuStates.psycho)
        

# from test_utils import STRESS_WORDS

# @router.message(botstates.MainMenuStates.tests)
# async def tests_choice(message: types.Message, state: FSMContext):
#     if message.text.lower() == "орфоэпия":
#         await state.set_state(botstates.Tests.rus_orfoepia)
#         word = test_utils.get_stress_word()
#         await message.answer("Напишите слово с правильно поставленным ударением, отметив ударение заглавной буквой: \n\n" + word.lower() 
#         + "\n\n Чтобы остановить тренажёр, напишите 'Стоп'")
#         await state.update_data(current_word=word)
#     else:
#         await state.set_state(botstates.MainMenuStates.main)
#         await message.answer("Ещё в разработке✅", reply_markup=kb.main_menu_keyboard)

# @router.message(botstates.Tests.rus_orfoepia)
# async def rus_orfoepia_test(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     word = test_utils.get_stress_word()
#     if message.text == None:
#         cword = data["current_word"]
#         await message.answer(f"Неверно! Правильное написание: <b>{cword}</b>\n Следующее слово: <b>" + word.lower() + "</b>")
#         return
#     if message.text in STRESS_WORDS and message.text.lower() == data["current_word"].lower():
#         await message.answer("Верно! \n Следующее слово: " + word.lower())
#     elif message.text.lower() == "стоп":
#         await state.set_state(botstates.MainMenuStates.main)
#         await message.answer("Тестирование окончено", reply_markup=kb.main_menu_keyboard)
#     else:
#         cword = data["current_word"]
#         await message.answer(f"Неверно! Правильное написание: {cword}\n Следующее слово: " + word.lower())
#     data["current_word"] = word
#     await state.update_data(data)