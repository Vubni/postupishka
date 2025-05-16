from typing import List, Optional
from asyncpg import Record
from database.database import Database
from core import generate_unique_code
from aiohttp import web
import config

async def check_token(token):
    async with Database() as db:
        await db.execute("DELETE FROM tokens WHERE date < CURRENT_DATE - INTERVAL '1 month'")
        res = await db.execute("SELECT email FROM tokens WHERE token=$1", (token,))
        if not res:
            return web.Response(status=401, text="Invalid token")
    return res["email"]

async def register_user(email : str, password : str, first_name: str, class_number : int) -> str:
    """Регистрация нового пользователя в системе

    Args:
        first_name (str): _description_
        email (str): _description_
        password (str): _description_
        class_number (int): _description_

    Returns:
        str: _description_
    """
    async with Database() as db:
        res = await db.execute("SELECT 1 FROM users WHERE email = $1", (email,))
        if res:
            return web.Response(status=409, text="The email has already been registered")
        
        await db.execute(
            "INSERT INTO users (first_name, email, password, class) VALUES ($1, $2, $3, $4)",
            (first_name, email, password, class_number)
        )
        await db.execute("DELETE FROM tokens WHERE date < CURRENT_DATE - INTERVAL '1 month'")
        code = generate_unique_code()
        await db.execute("INSERT INTO tokens (email, token) VALUES ($1, $2)", (email, code,))
        await db.execute("INSERT INTO subjects (email, subject) VALUES ($1, $2)", (email, "Русский язык",))
    return code
            
async def auth(identifier:str, password:str) -> str:
    async with Database() as db:
        res = await db.execute("SELECT email FROM users WHERE (email = $1 or first_name = $1) AND password=$2", (identifier, password))
        if not res:
            return web.Response(status=401, text="The login information is incorrect")
        email = res["email"]
        await db.execute("DELETE FROM tokens WHERE date < CURRENT_DATE - INTERVAL '1 month'")
        code = generate_unique_code()
        await db.execute("INSERT INTO tokens (email, token) VALUES ($1, $2)", (email, code,))
    return code


async def profile_get(email):
    async with Database() as db:
        res = await db.execute("SELECT * FROM users WHERE email=$1", (email,))
    return res

async def profile_delete(email):
    async with Database() as db:
        res = await db.execute("SELECT * FROM users WHERE email=$1", (email,))
        if not res:
            return web.json_response({"error": "Profile not found"}, status=404)
        await db.execute("DELETE FROM users WHERE email=$1", (email,))
    return web.Response(status=204)

async def profile_edit(email:str, email_new:str, first_name:str, password_old:str, password_new:str, class_number:int, subjects:list):
    async with Database() as db:
        if email_new:
            await db.execute("UPDATE users SET email=$2 WHERE email=$1", (email, email_new))
        if first_name:
            await db.execute("UPDATE users SET first_name=$2 WHERE email=$1", (email, first_name))
        if password_old and password_new:
            res = await db.execute("UPDATE users SET password=$3 WHERE email=$1 AND password=$2", (email, password_old, password_new))
            if not res:
                return web.json_response({"name": "password_old", "error": "Password is incorrect"}, status=400)
        if class_number:
            await db.execute("UPDATE users SET class=$2 WHERE email=$1", (email, class_number))
        if subjects:
            if subjects != await db.execute("SELECT subject, current_score, desired_score FROM subjects WHERE email = $1", (email,)):
                await db.execute("DELETE FROM subjects WHERE email=$1", (email,))
                for item in subjects:
                    await db.execute("INSERT INTO subjects (email, subject, current_score, desired_score) VALUES ($1, $2, $3, $4)", (email, item["subject"], item["current_score"], item["desired_score"]))
    return web.Response(status=204)
    

async def get_subjects(email: str) -> Optional[List[Record]]:
    async with Database() as db:
        return await db.execute_all("SELECT subject, current_score, desired_score FROM subjects WHERE email = $1", (email,))
    
async def get_tg_url(email: str):
    async with Database() as db:
        res = await db.execute("SELECT code FROM temp_tg_url WHERE email=$1", (email,))
        if not res:
            code = generate_unique_code(16)
            await db.execute("INSERT INTO temp_tg_url (email, code) VALUES ($1, $2)", (email, code))
        else:
            code = res["code"]
    return config.bot_url + "?start=" + code
