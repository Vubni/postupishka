import os
from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec,
    validation_middleware
)
import aiohttp_cors
from config import logger
import asyncio
from api import (profile, auth, telegram, specialization, university, schedule, psychologist)

async def ip_filter_middleware(app, handler):
    async def middleware(request):
        # Временно разрешаем все запросы на момент конкурса
        return await handler(request)
    
        # if request.path in ('/doc', '/swagger.json'):
        #     return await handler(request)

        # allowed_origins = ['https://online-postupishka.ru']
        # origin = request.headers.get('Origin') or request.headers.get('Referer')

        # if origin and any(origin.startswith(allowed) for allowed in allowed_origins):
        #     return await handler(request)

        # logger.warning(f"Доступ запрещен для Origin: {origin}")
        # return web.Response(status=403, text="Access denied")
    return middleware

if __name__ == "__main__":
    app = web.Application()

    cors = aiohttp_cors.setup(app, defaults={
        "https://online-postupishka.ru": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE"]
        )
    })
    
    setup_aiohttp_apispec(
        app,
        title="API doc",
        version="v1",
        url="/swagger.json",
        swagger_path="/doc",
        security_definitions={
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Bearer token authorization"
            }
        }
    )

    prefix = "/"
    routes = [
        web.post(prefix + 'reg', auth.register),
        web.post(prefix + 'auth', auth.auth),
        web.post(prefix + 'email', auth.email_verify),
        
        
        web.get(prefix + 'profile', profile.profile_get),
        web.patch(prefix + 'profile', profile.profile_patch),
        web.delete(prefix + 'profile', profile.profile_delete),
        
        web.post(prefix + 'psychologist', psychologist.question),
        web.get(prefix + 'psychologist', psychologist.get),
        
        web.post(prefix + 'university/add', university.add_university),
        web.get(prefix + 'university', university.get_university),
        # web.delete(prefix + 'university', university.del_university),
        # web.post(prefix + 'university/update', university.update_university),
        
        # web.get(prefix + 'telegram', None),
        # web.delete(prefix + 'telegram', None),
        web.get(prefix + 'telegram/url', telegram.get_tg_url),
        
        web.post(prefix + 'schedule', schedule.add),
        web.get(prefix + 'schedule', schedule.get),
        
        web.get(prefix + 'specialization/question', specialization.question),
        web.post(prefix + 'specialization/answer', specialization.answer),
        web.get(prefix + 'specialization/result', specialization.get_result),
        web.get(prefix + 'specialization', specialization.get_timer),
        
        # web.get('/{path:.*}', handle_get_file)
    ]
    
    for route in routes:
        cors.add(app.router.add_route(route.method, route.path, route.handler))

    app.middlewares.append(validation_middleware)
    app.middlewares.append(ip_filter_middleware)
    
    logger.info("Запуск сервера. . .")
    web.run_app(
        app,
        host=os.environ.get('INSTANCE_HOST', 'localhost'),
        port=int(os.environ.get('PORT', 8080))
    )