import sqlite3
import pandas as pd
from fastapi import FastAPI, WebSocket , Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from fastapi.staticfiles import StaticFiles
import json
import asyncio
import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static/css", StaticFiles(directory="templates/assets/css"), name="static")
app.mount("/static/js", StaticFiles(directory="templates/assets/js"), name="js")
app.mount("/static/images", StaticFiles(directory="templates/images"), name="images")

def convert(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

# Function to fetch data from MySQL
async def get_data_from_db():
    conn = sqlite3.connect('lighteconomy.db')
    cursor = conn.cursor()
    query = '''
        SELECT m.name, m.money, b.level as banklevel,b.money as bankmoney
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

async def get_data_from_db2():
    conn = sqlite3.connect('LoginSecurity.db')
    cursor = conn.cursor()
    query = '''
        SELECT p.last_name,p.last_login,p.registration_date
        FROM ls_players p
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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generic", response_class=HTMLResponse)
async def generic(request: Request):
    return templates.TemplateResponse("generic.html", {"request": request})

@app.get("/elements", response_class=HTMLResponse)
async def generic(request: Request):
    return templates.TemplateResponse("elements.html", {"request": request})


@app.websocket("/money_ws")
async def money_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data_from_db = await get_data_from_db()
        money_data = [{"name": item["name"], "money": item["money"]} for item in data_from_db]
        await websocket.send_text(json.dumps(money_data))
        await asyncio.sleep(10)

@app.websocket("/level_ws") # level_ws경로에 websocket연결 처리 함수 
async def level_websocket_endpoint(websocket: WebSocket): # 클라이언트가 websocket연결 시도하면 함수 실행(비동기)
    await websocket.accept() # 클라이언트의 websoket 연결 수락 

    while True:
        data_from_db = await get_data_from_db()
        level_data = [{"name": item["name"], "level": item["banklevel"]} for item in data_from_db]
        await websocket.send_text(json.dumps(level_data)) #websoket을 통해 클라이언트로 보냄
        await asyncio.sleep(10)

@app.websocket("/bankmoney_ws") 
async def bankmoney_websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 

    while True:
        data_from_db = await get_data_from_db()
        level_data = [{"name": item["name"], "bankmoney": item["bankmoney"]} for item in data_from_db]
        await websocket.send_text(json.dumps(level_data)) #websoket을 통해 클라이언트로 보냄
        await asyncio.sleep(10)

@app.websocket("/bankmoney2_ws") 
async def lbankmoney2_websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 

    while True:
        data_from_db = await get_data_from_db()
        level_data = [{"name": item["name"], "bankmoney": item["bankmoney"]} for item in data_from_db]
        await websocket.send_text(json.dumps(level_data)) #websoket을 통해 클라이언트로 보냄
        await asyncio.sleep(10)

@app.websocket("/level2_ws") 
async def level2_websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 

    while True:
        data_from_db = await get_data_from_db()
        level_data = [{"name": item["name"], "level": item["banklevel"]} for item in data_from_db]
        await websocket.send_text(json.dumps(level_data)) #websoket을 통해 클라이언트로 보냄
        await asyncio.sleep(10)

@app.websocket("/moneylevel_ws")
async def moneylevel_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data_from_db = await get_data_from_db()
        money_data = [
    {
        "name": item["name"],
        "money": (item['money'] / (item['money'] + item['bankmoney'])) if (item['money'] + item['bankmoney']) != 0 else 1,
        "bankmoney": (item['bankmoney'] / (item['money'] + item['bankmoney'])) if (item['money'] + item['bankmoney']) != 0 else 1  # 0으로 나누는 것을 피하기 위한 조건 추가
    }
    for item in data_from_db]
        await websocket.send_text(json.dumps(money_data))
        await asyncio.sleep(10)

# @app.websocket("/userCountText_ws")
# async def userCountText_websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     while True:
#         data_from_db = await get_data_from_db()
#         money_data = [{"count user": len(item["name"])} for item in data_from_db]
#         await websocket.send_text(json.dumps(money_data))
#         await asyncio.sleep(10)

@app.websocket("/userline_ws")
async def userline_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data_from_db = await get_data_from_db2()
        login_data = [{'name':item['last_name'],'last_login':convert(item['last_login']),'registration_login':convert(item['registration_date'])} for item in data_from_db]
        await websocket.send_text(json.dumps(login_data))
        await asyncio.sleep(10)