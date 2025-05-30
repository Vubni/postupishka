from .create_bot import bot, dp, scheduler
from .handlers.main import router
# from telegram.callback.main import router as router_call
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.database import Database

async def notification():
    async with Database() as db:
        await db.execute("""SELECT s.*
FROM schedule s
JOIN users u ON s.email = u.email
WHERE u.telegram_id IS NOT NULL;""")

async def main():
    scheduler.add_job(
        notification,
        CronTrigger(second=0)
    )
    scheduler.start()
    
    dp.include_router(router)
    # dp.include_router(router_call)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())