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

@docs(
    tags=["Specialization"],
    summary="Генерация вопроса",
    description="Генерация вопроса для определения специализации",
    responses={
        200: {"description": "Вопрос успешно сгенерирован", "schema": sh.QuestionSchema},
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
async def question(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        result = await func.generate_question(email)
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error("auth error: ", e)
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
async def answer(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        try:
            request_data = await request.json()
            answer = request_data.get('answer')
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        
        res = func.add_answer(email, answer)
        if not res:
            return web.json_response({"error": "Not a single question has been asked! Nothing to answer."}, status=400)
        return web.Response(status=204)
    except Exception as e:
        logger.error("auth error: ", e)
        return web.Response(status=500, text=str(e))
    
@docs(
    tags=["Specialization"],
    summary="Получить результат тестирования",
    description="После ответа на все вопросы - вы сможете получить результаты тестирования и специализации на выбор (можно не отвечать на все вопросы и вызвать преждевременно)",
    responses={
        200: {"description": "Результат успешно выдан", "schema": sh.UniversitySchema(many=True)},
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
        if type(email) != str:
            return email
        
        result = func.get_result(email)
        if not result:
            return web.json_response({"error": "Not a single question has been asked! Nothing to answer."}, status=400)
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error("auth error: ", e)
        return web.Response(status=500, text=str(e))