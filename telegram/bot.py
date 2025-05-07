from telegram.create_bot import bot, dp
from telegram.handlers.main import router
# from telegram.callback.main import router as router_call


# back worjk
async def main():
    dp.include_router(router)
    # dp.include_router(router_call)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())