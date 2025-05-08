from aiohttp import web
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
)
from config import logger
from docs import schems as sh
from database import functions as func_db
import core
from telegram.create_bot import bot

@docs(
    tags=["Profile"],
    summary="Получение профиля",
    description="Возвращает информацию о пользователе. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        200: {"description": "Профиль успешно получен", "schema": sh.UserProfileSchema},
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
async def profile_get(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        res = await func_db.profile_get(email)
        result = {"email": res["email"],
            "first_name": res["first_name"],
            "class": res["class"]}
        if res["telegram_id"]:
            result["username"] = (await bot.get_chat(res["telegram_id"])).username
        result["subjects"] = await func_db.get_subjects(email)
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e))
    
    
@docs(
    tags=["Profile"],
    summary="Удаление профиля",
    description="Удаляет профиль. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        204: {"description": "Профиль успешно удалён"},
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
async def profile_delete(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        return await func_db.profile_delete(email)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e))
    
    
@docs(
    tags=["Profile"],
    summary="Изменение профиля",
    description="Изменяет профиль. Для доступа требуется Bearer-токен в заголовке Authorization",
    responses={
        204: {"description": "Профиль успешно изменён"},
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
@request_schema(sh.UserEditSchema)
async def profile_patch(request: web.Request) -> web.Response:
    try:
        email = await core.check_authorization(request)
        if type(email) != str:
            return email
        
        try:
            request_data = await request.json()
            email_new = request_data.get('email', None)
            first_name = request_data.get('firstName', None)
            password_old = request_data.get('password_old', None)
            password_new = request_data.get('password_new', None)
            class_number = request_data.get('class', None)
            if class_number:
                class_number = int(class_number)
            subjects = request_data.get('subjects', None)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=400)
        
        if (password_old and not password_new) or (not password_old and password_new):
            return web.json_response({"name": "password", "error": "only one of the password_new or password_old fields cannot be specified"}, status=400)
        if not class_number and not email_new and not first_name and (not password_old or not password_new) and not subjects:
            return web.json_response({"error": "no parametrs"}, status=400)
        
        if email_new and (len(email_new) > 256):
            return web.json_response({"error": "email must not exceed 256 characters in length."}, status=400)
        if email_new and (not core.is_valid_email(email_new)):
            return web.json_response({"error": "Expected a valid email address."}, status=422)
        if class_number and (class_number < 9 or class_number > 11):
            return web.json_response({"error": "The class number cannot be outside the range of 9-11."}, status=400)
        if type(subjects) != list:
            return web.json_response({"name": "subjects", "error": "The list type is expected"}, status=400)
            
        
        return await func_db.profile_edit(email, email_new, first_name, password_old, password_new, class_number, subjects)
    except Exception as e:
        logger.error("profile error: ", e)
        return web.Response(status=500, text=str(e))