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
async def register(request: web.Request) -> web.Response:
    try:
        try:
            request_data = await request.json()
            class_number = request_data.get('class')
            email = request_data.get('email')
            first_name = request_data.get('firstName')
            password = request_data.get('password')
        except:
            return web.json_response(status=400)
        
        if len(email) > 256:
            return web.json_response({"name": "email", "error": "email must not exceed 256 characters in length."}, status=400)
        if not core.is_valid_email(email):
            return web.json_response({"name": "email", "error": "Expected a valid email address."}, status=422)
        if class_number < 9 or class_number > 11:
            return web.json_response({"name": "class", "error": "The class number cannot be outside the range of 9-11."}, status=400)
        if type(email) is not str:
            return web.json_response({"name": "email", "error": "The str type is expected"}, status=400)
        if type(first_name) is not str:
            return web.json_response({"name": "first_name", "error": "The str type is expected"}, status=400)
        if type(password) is not str:
            return web.json_response({"name": "password", "error": "The str type is expected"}, status=400)
        if type(class_number) is not int:
            return web.json_response({"name": "class", "error": "The int type is expected"}, status=400)
        
        code = await func_db.register_user(email, password, first_name, class_number)
        if type(code) != str:
            return code
        return web.json_response({"token": code}, status=201)
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
async def auth(request: web.Request) -> web.Response:
    try:
        try:
            request_data = await request.json()
            identifier = request_data.get('identifier')
            password = request_data.get('password')
        except:
            return web.json_response(status=400)
        
        if len(identifier) > 256:
            return web.json_response({"error": "identifier must not exceed 256 characters in length."}, status=400)
        if type(identifier) is not str:
            return web.json_response({"name": "identifier", "error": "The str type is expected"}, status=400)
        if type(password) is not str:
            return web.json_response({"name": "password", "error": "The str type is expected"}, status=400)
        
        code = await func_db.auth(identifier, password)
        if type(code) != str:
            return code
        return web.json_response({"token": code}, status=200)
    except Exception as e:
        logger.error("auth error: ", e)
        return web.Response(status=500, text=str(e))