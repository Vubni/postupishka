from database.database import Database
import json

async def add_university(email, university, direction, scores):
    async with Database() as db:
        res = await db.execute("SELECT COUNT(*) FROM specializations WHERE email=$1", (email,))
        if res["count"] >= 5:
            return False
        await db.execute("INSERT INTO specializations (email, university, direction, scores) VALUES ($1, $2, $3, $4)", (email, university, direction, json.dumps(scores)))
    return True

async def get_university(email):
    async with Database() as db:
        result = await db.execute_all("SELECT university, direction, scores FROM specializations WHERE email=$1", (email,))
    for res in result:
        res["scores"] = json.loads(res["scores"])
    return result