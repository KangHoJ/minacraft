import sqlite3
import pandas as pd
from fastapi import FastAPI, WebSocket , Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
import json
import asyncio
from datetime import datetime

def convert(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')


# SQLite 데이터베이스에 연결
conn = sqlite3.connect('LoginSecurity.db')
conn2 = sqlite3.connect('lighteconomy.db')
cursor = conn.cursor()
cursor2 = conn2.cursor()

query = '''
        SELECT p.last_name,p.last_login,p.registration_date
        FROM ls_players p
    '''
cursor.execute(query)
result = cursor.fetchall()
columns = [column[0] for column in cursor.description]

result_list = []
for row in result:
    result_dict = dict(zip(columns, row))
    result_list.append(result_dict)

query2 = '''
        SELECT m.name, m.money, b.level as banklevel,b.money as bankmoney
        FROM BankTable b
        INNER JOIN MoneyTable m ON b.name = m.name
    '''
cursor2.execute(query2)
result2 = cursor2.fetchall()
columns2 = [column[0] for column in cursor2.description]

result_list2 = []
for row in result2:
    result_dict2 = dict(zip(columns2, row))
    result_list2.append(result_dict2)

cursor.close()
conn.close()
cursor2.close()
conn2.close()

print(result_list)
print(result_list2)

# print('----'*50)
login_data = json.dumps([{'name':item['last_name'],'last_login':convert(item['last_login']),'registration_login':convert(item['registration_date'])} for item in result_list])
login_data2 = json.dumps([{'money':item['money'],'banklevel':item['banklevel']} for item in result_list2])
print(login_data)
print(login_data2)
# print(tlogin_data)




