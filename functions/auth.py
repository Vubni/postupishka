from typing import List, Optional
from asyncpg import Record
from database.database import Database
from core import generate_unique_code
from aiohttp import web
import config

async def verify_email(email):
    async with Database() as db:
        await db.execute("UPDATE users SET verified=true WHERE email=$1", (email,))

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
            return web.json_response({"name": "email", "error": "The email has already been registered"}, status=409)
        res = await db.execute("SELECT 1 FROM users WHERE first_name = $1", (first_name,))
        if res:
            return web.json_response({"name": "first_name", "error": "The first_name has already been registered"}, status=409)
        
        await db.execute(
            "INSERT INTO users (first_name, email, password, class_number) VALUES ($1, $2, $3, $4)",
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
    return web.json_response({"token": code}, status=200)


async def profile_get(email):
    async with Database() as db:
        res = await db.execute("SELECT email, first_name, class_number, verified, telegram_id FROM users WHERE email=$1", (email,))
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
            res = await db.execute("SELECT 1 FROM users WHERE email = $1", (email_new,))
            if res:
                return web.json_response({"name": "email", "error": "The email has already been registered"}, status=409)
            await db.execute("UPDATE users SET email=$2 WHERE email=$1", (email, email_new))
            email = email_new
        if first_name:
            res = await db.execute("SELECT 1 FROM users WHERE first_name = $1", (first_name,))
            if res:
                return web.json_response({"name": "first_name", "error": "The first_name has already been registered"}, status=409)
            await db.execute("UPDATE users SET first_name=$2 WHERE email=$1", (email, first_name))
        if password_old and password_new:
            res = await db.execute("SELECT 1 FROM users WHERE email=$1 AND password=$2", (email, password_old))
            if not res:
                return web.json_response({"error": "Password is incorrect", "errors": [{"name": "password_old", "type": "incorrect", "message": "Password is incorrect", "value": password_old}]}, status=400)
            await db.execute("UPDATE users SET password=$3 WHERE email=$1 AND password=$2", (email, password_old, password_new))
        if class_number:
            await db.execute("UPDATE users SET class_number=$2 WHERE email=$1", (email, class_number))
        if subjects:
            if subjects != await db.execute("SELECT subject, current_score, desired_score FROM subjects WHERE email = $1", (email,)):
                await db.execute("DELETE FROM subjects WHERE email=$1", (email,))
                for item in subjects:
                    await db.execute("INSERT INTO subjects (email, subject, current_score, desired_score) VALUES ($1, $2, $3, $4)", (email, item["subject"], int(item["current_score"]), int(item["desired_score"])))
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
