import sqlite3
import pandas as pd
from fastapi import FastAPI, WebSocket , Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
import json
import asyncio

async def get_data_from_db():
    conn = sqlite3.connect('lighteconomy.db')
    cursor = conn.cursor()

    query = '''
        SELECT m.name, b.level, m.money  
        FROM BankTable b
        INNER JOIN MoneyTable m ON b.name = m.name
    '''
    cursor.execute(query)
    result = cursor.fetchall() # 행결과 튜플
    columns = [column[0] for column in cursor.description] #컬럼들 
    result_list = []
    for row in result:
        result_dict = dict(zip(columns, row))
        result_list.append(result_dict)
    cursor.close()
    conn.close()
    return result_list


async def main():
    result_list = await get_data_from_db()
    level_data = [{'name':i['name'],'money':i['money']} for i in result_list]
    print(json.dumps(level_data))

if __name__ =="__main__":
    import asyncio
    asyncio.run(main())