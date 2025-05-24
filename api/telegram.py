from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from config import logger
from docs import schems as sh
from functions import auth as func_db
import core
from telegram.create_bot import bot

@docs(
    tags=["Telegram"],
    summary="Получение ссылки для привязки телеграм аккаунта",
    description="Возвращает информацию о пользователе. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        200: {"description": "Ссылка успешно получена или аккаунт уже привязан", "schema": sh.TgUrlSchema},
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
async def get_tg_url(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        url = await func_db.get_tg_url(email)
        return web.json_response({"url": url}, status=200)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e))