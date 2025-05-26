from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from config import logger
from docs import schems as sh
from functions import auth as func_db
from api import validate

@docs(
    tags=["Auth"],
    summary="Регистрация пользователя",
    description="Регистрация нового пользователя с указанием класса и контактов",
    responses={
        201: {"description": "Регистрация успешно выполнена", "schema": sh.TokenResponseSchema},
        400: {"description": "Отсутствует один из параметров или ограничения параметра не выполнены", "schema": sh.Error400Schema},
        409: {"description": "Логин или почта заняты"},
        422: {"description": "Переданный email не соответствует стандартам электронной почты"},
        500: {"description": "Server-side error (Ошибка на стороне сервера)"}
    }
)
@request_schema(sh.UserRegisterSchema)
@validate.validate(validate.Register)
async def register(request: web.Request, parsed : validate.Register) -> web.Response:
    try:
        email = parsed.email
        class_number = parsed.class_number
        first_name = parsed.first_name
        password = parsed.password
        
        code = await func_db.register_user(email, password, first_name, class_number)
        return code
    except Exception as e:
        logger.error("register error: ", e)
        return web.Response(status=500, text=str(e))

@docs(
    tags=["Auth"],
    summary="Авторизация пользователя",
    description="Получение токена авторизации",
    responses={
        200: {"description": "Авторизация успешно выполнена", "schema": sh.TokenResponseSchema},
        400: {"description": "Отсутствует один из параметров или ограничения параметра не выполнены", "schema": sh.Error400Schema},
        401: {"description": "Логин или почта не зарегистрированы"},
        500: {"description": "Server-side error (Ошибка на стороне сервера)"}
    }
)
@request_schema(sh.UserAuthSchema)
@validate.validate(validate.Auth)
async def auth(request: web.Request, parsed : validate.Auth) -> web.Response:
    try:
        identifier = parsed.identifier
        password = parsed.password
        
        code = await func_db.auth(identifier, password)
        return code
    except Exception as e:
        logger.error("auth error: ", e)
        return web.Response(status=500, text=str(e))