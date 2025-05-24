from database.database import Database
from aiohttp import web

async def check_token(token):
    async with Database() as db:
        await db.execute("DELETE FROM tokens WHERE date < CURRENT_DATE - INTERVAL '1 month'")
        res = await db.execute("SELECT email FROM tokens WHERE token=$1", (token,))
        if not res:
            return web.Response(status=401, text="Invalid token")
    return res["email"]
