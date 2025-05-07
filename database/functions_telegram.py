from typing import List, Optional
from asyncpg import Record
from database.database import Database
from core import generate_unique_code
from aiohttp import web
import config

async def check_connect(user_id:int) -> bool:
    async with Database() as db:
        res = await db.execute("SELECT * FROM users WHERE telegram_id=$1", (user_id,))
    return True if res else False