from database.database import Database

async def add_university(email, university, direction, scores):
    async with Database() as db:
        res = await db.execute("SELECT COUNT(*) FROM specializations WHERE email=$1", (email,))
        if res["count"] >= 5:
            return False
        await db.execute("INSERT INTO specializations (university, direction, scores) VALUES ($1, $2, $3)", (university, direction, scores))
    return True