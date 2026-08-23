# from fastmcp import FastMCP
# import random
# mcp = FastMCP(name='Demo_server')

# @mcp.tool
# def rool_dice(n_dice: int) -> list[int]:
#     "this function use to rolle n_dice"
#     return [random.randint(1,6) for i in range(n_dice)]

# @mcp.tool
# def add(a: float,b: float) -> float:
#     'this function add tow numbers'
#     return a+b

# if __name__ == "__main__":
#     mcp.run()



from fastmcp import FastMCP
import sqlite3
import os
import aiosqlite
import asyncio
import tempfile
mcp = FastMCP(name='expainse_tracker')
path = os.path.join(tempfile.gettempdir(),'data.db')
try:
    async def create():

        async with aiosqlite.connect(path) as f:
            await f.execute("""
                    CREATE TABLE IF NOT EXISTS expense (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        subcategory TEXT DEFAULT ''
                    );
                    """)
                    

except Exception as e:
    raise Exception(f"Error initializing the database: {e}")
create()
@mcp.tool
async def add_expense(date ,amount: int,category: str,subcategory: str):
        'this function use to add expense in expense tracker'
        async with aiosqlite.connect(path) as f:
                cur = await f.execute("INSERT INTO expense(date,amount,category,subcategory) VALUES (?,?,?,?)",
                                (date,amount,category,subcategory))
                return {'status':'ok','id':cur.lastrowid}


@mcp.tool
async def list_all_expense():
    'this function return all expense data'
    async with aiosqlite.connect(path) as f:
        data = await f.execute("SELECT id,date,amount,category,subcategory FROM expense ORDER BY id ASC")
        cur = [d[0] for d in data.description]
        return [dict(zip(cur,r)) for r in await data.fetchall()]


@mcp.tool
async def list_expense_in_range(st,ed):
    'this function return expense in range of dates form data'
    async with aiosqlite.connect(path) as f:
        data = await f.execute("SELECT id,date,amount,category,subcategory FROM expense WHERE date BETWEEN ? AND ? ORDER BY id ASC",
                         (st,ed))
        cur = [d[0] for d in data.description]
        return [dict(zip(cur,r)) for r in await data.fetchall()]

if __name__ == '__main__':

    mcp.run()
