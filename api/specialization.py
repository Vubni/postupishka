from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from config import logger
from docs import schems as sh
from functions import specialization as func
import core
from api import validate
from datetime import datetime, timedelta
import pytz

@docs(
    tags=["Specialization"],
    summary="Генерация вопроса",
    description="Генерация вопроса для определения специализации",
    responses={
        200: {"description": "Вопрос успешно сгенерирован", "schema": sh.QuestionSchema},
        400: {"description": "Отсутствует один из параметров или ограничения параметра не выполнены", "schema": sh.Error400Schema},
        401: {"description": "Логин или почта не зарегистрированы"},
        409: {"description": "Временная блокировка после прошлого определения специализации ещё не закончилась"},
        500: {"description": "Server-side error (Ошибка на стороне сервера)"}
    },
    parameters=[{
        'in': 'header',
        'name': 'Authorization',
        'schema': {'type': 'string', 'format': 'Bearer'},
        'required': True,
        'description': 'Bearer-токен для аутентификации'
    }]
)
async def question(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if not isinstance(email, str):
            return email
        
        day_old = await func.get_time(email)
        if day_old:
            seconds_difference, days, hours, minutes = time_processing(day_old)
            if seconds_difference <= 0:
                return web.json_response({"error": "Timer is not finish"}, status=409)
        
        result = await func.generate_question(email)
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error("question error: ", e)
        return web.Response(status=500, text=str(e))
    
    
@docs(
    tags=["Specialization"],
    summary="Отправка ответа на вопрос",
    description="Отправьте ответ на последний сгенерированный вопрос",
    responses={
        204: {"description": "Ответ успешно записан"},
        400: {"description": "Отсутствует один из параметров или ограничения параметра не выполнены", "schema": sh.Error400Schema},
        401: {"description": "Логин или почта не зарегистрированы"},
        500: {"description": "Server-side error (Ошибка на стороне сервера)"}
    },
    parameters=[{
        'in': 'header',
        'name': 'Authorization',
        'schema': {'type': 'string', 'format': 'Bearer'},
        'required': True,
        'description': 'Bearer-токен для аутентификации'
    }]
)
@request_schema(sh.AnswerAddSchema)
@validate.validate(validate.Spec_answer)
async def answer(request: web.Request, parsed : validate.Spec_answer) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if not isinstance(email, str):
            return email

        answer = parsed.answer
        
        res = func.add_answer(email, answer)
        if not res:
            return web.json_response({"error": "Not a single question has been asked! Nothing to answer."}, status=400)
        return web.Response(status=204)
    except Exception as e:
        logger.error("answer error: ", e)
        return web.Response(status=500, text=str(e))
    
@docs(
    tags=["Specialization"],
    summary="Получить результат тестирования",
    description="После ответа на все вопросы - вы сможете получить результаты тестирования и специализации на выбор (можно не отвечать на все вопросы и вызвать преждевременно)",
    responses={
        200: {"description": "Результат успешно выдан", "schema": sh.UniversitySchema},
        202: {"description": "Результат успешно выдан", "schema": sh.University_load},
        400: {"description": "Отсутствует один из параметров или ограничения параметра не выполнены", "schema": sh.Error400Schema},
        401: {"description": "Логин или почта не зарегистрированы"},
        500: {"description": "Server-side error (Ошибка на стороне сервера)"}
    },
    parameters=[{
        'in': 'header',
        'name': 'Authorization',
        'schema': {'type': 'string', 'format': 'Bearer'},
        'required': True,
        'description': 'Bearer-токен для аутентификации'
    }]
)
async def get_result(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if not isinstance(email, str):
            return email
        
        result = await func.get_result_handler(email)
        if not result:
            return web.json_response({"error": "Not a single question has been asked! Nothing to answer."}, status=400)
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error("get_result error: ", e)
        return web.Response(status=500, text=str(e))
    
    
def time_processing(day_old:datetime):
    day_old = day_old + timedelta(days=7)
    current_time = datetime.now(pytz.utc)
    time_difference = day_old - current_time
    
    seconds_difference = int(time_difference.total_seconds())
    days = seconds_difference // 86400
    hours = (seconds_difference % 86400) // 3600
    minutes = (seconds_difference % 3600) // 60
    
    return seconds_difference, days, hours, minutes
    
@docs(
    tags=["Specialization"],
    summary="Получить время до следующего запроса",
    description="После добавления вуза можно будет добавить новый только через 7 дней. Данный метод позволяет проверить - доступно ли добавление новых вузов.",
    responses={
        200: {"description": "Результат успешно выдан", "schema": sh.Specialization_timer},
        400: {"description": "Отсутствует один из параметров или ограничения параметра не выполнены", "schema": sh.Error400Schema},
        401: {"description": "Логин или почта не зарегистрированы"},
        500: {"description": "Server-side error (Ошибка на стороне сервера)"}
    },
    parameters=[{
        'in': 'header',
        'name': 'Authorization',
        'schema': {'type': 'string', 'format': 'Bearer'},
        'required': True,
        'description': 'Bearer-токен для аутентификации'
    }]
)
async def get_timer(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if not isinstance(email, str):
            return email
        
        day_old = await func.get_time(email)
        if not day_old:
            return web.Response(status=404)
        
        seconds_difference, days, hours, minutes = time_processing(day_old)
        if seconds_difference <= 0:
            return web.json_response({"days": 0, "hours": 0, "minutes": 0}, status=200)
        
        return web.json_response({"days": days, "hours": hours, "minutes": minutes}, status=200)
    
    except Exception as e:
        logger.error("get_result error: ", e)
        return web.Response(status=500, text=str(e))