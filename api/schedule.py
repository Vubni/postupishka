from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from config import logger
from docs import schems as sh
from functions import schedule as func
import core
from telegram.create_bot import bot

@docs(
    tags=["Shedule"],
    summary="Добавление информации о расписании",
    description="Добавляет информацию о необходимом расписании. Ожидается максимально подробная информация и занятиях на ближайшие дни, сразу выполняется перерасчёт расписания. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        201: {"description": "Информация о расписании успешно добавлена"},
        400: {"description": "Отсутствует один из параметров", "schema": sh.Error400Schema},
        401: {"description": "Авторизация не выполнена"},
        422: {"description": "Информация о расписании обработана, но не может быть сохранена", "schema": sh.CreateScheduleError},
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
@request_schema(sh.AddSchedule)
async def add(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        request_data = await request.json()
        try:
            content = str(request_data.get('content'))
        except Exception as e:
            return web.json_response({"name": "content", "error": "object is not passed or has an invalid type"}, status=400)
        
        res = await func.add_info(email, content)
        if not res["status"]:
            return web.json_response({"error": res["text"]}, status=200)
        return web.Response(status=204)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e))
    

@docs(
    tags=["Shedule"],
    summary="Получение расписания",
    description="Возвращает расписание для пользователя на текущую и на следующую неделю, если такое есть. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        200: {"description": "Списокв направлений", "schema": sh.GetSchedule(many=True)},
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
        
        res = list(await func.get_info(email))
        return web.json_response(res, status=200)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e)) 