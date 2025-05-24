from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from config import logger
from docs import schems as sh
from functions import psychologist as func_db
import core

@docs(
    tags=["Psychologist"],
    summary="Задать вопрос",
    description="Отправьте вопрос и получите ответ от психолога. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        200: {"description": "Вопрос успешно обработан", "schema": sh.AnswerAddSchema},
        400: {"description": "Отсутствует один из параметров", "schema": sh.Error400Schema},
        401: {"description": "Авторизация не выполнена"},
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
@request_schema(sh.QuestionSchema_Psycho)
async def question(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        try:
            request_data = await request.json()
            question = request_data.get('question', None)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        
        if type(question) is not str:
            return web.json_response({"name": "question", "error": "Type is not string"}, status=400)
        
        result = await func_db.question(email, question)
        return web.json_response({"answer": result}, status=200)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e))
    
@docs(
    tags=["Psychologist"],
    summary="Получить диалог",
    description="Получить историю диалога (до 10 сообщений включительно). Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        200: {"description": "Вопрос успешно обработан", "schema": sh.AiDialog(many=True)},
        400: {"description": "Отсутствует один из параметров", "schema": sh.Error400Schema},
        401: {"description": "Авторизация не выполнена"},
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
async def get(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        result = await func_db.dialog(email)
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e))