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
from api import validate

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
@validate.validate(validate.Univer_add)
async def add_university(request: web.Request, parsed : validate.Univer_add) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if not isinstance(email, str):
            return email
        
        university = parsed.university
        direction = parsed.direction
        scores = parsed.scores
        
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
        200: {"description": "Списокв направлений", "schema": sh.GetUniversity(many=True)},
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
        if not isinstance(email, str):
            return email
        
        res = list(await func.get_university(email))
        return web.json_response(res, status=200)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e)) 