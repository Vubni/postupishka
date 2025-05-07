from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from config import logger
from docs import schems as sh
from functions import university as func
import core
from telegram.create_bot import bot

@docs(
    tags=["University"],
    summary="Добавление направления в профиль",
    description="Добавляет вуз как цель пользователю. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        204: {"description": "Направление успешно добавлено"},
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
@request_schema(sh.AddUniversity)
async def add_university(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        request_data = await request.json()
        try:
            university = str(request_data.get('university'))
        except Exception as e:
            return web.json_response({"name": "university", "error": "object is not passed or has an invalid type"}, status=400)
        try:
            direction = str(request_data.get('direction'))
        except Exception as e:
            return web.json_response({"name": "direction", "error": "object is not passed or has an invalid type"}, status=400)
        try:
            scores = list(request_data.get('scores'))
            scores["min"], scores["avg"], scores["bud"]
        except Exception as e:
            return web.json_response({"name": "scores", "error": "object is not passed or has an invalid type"}, status=400)
        
        res = await func.add_university(email, university, direction, scores)
        if not res:
            return web.json_response({"error": "The maximum limit of 5 entries has been exceeded."}, status=409)
        return web.Response(status=204)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e))
    

@docs(
    tags=["University"],
    summary="Получение списка направлений",
    description="Возвращает список направлений выбранных пользователем. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        200: {"description": "Списокв направлений", "schema": sh},
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
async def get_university(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        res = await func.get_university(email)
        if not res:
            return web.json_response({"error": "The maximum limit of 5 entries has been exceeded."}, status=409)
        return web.Response(status=204)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e)) 