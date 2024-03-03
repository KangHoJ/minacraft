import sqlite3
import pandas as pd
from fastapi import FastAPI, WebSocket , Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from fastapi.staticfiles import StaticFiles
import json
import asyncio
from fastapi.encoders import jsonable_encoder
import datetime


db_config = # db 정보 


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static/css", StaticFiles(directory="templates/assets/css"), name="static")
app.mount("/static/js", StaticFiles(directory="templates/assets/js"), name="js")
app.mount("/static/images", StaticFiles(directory="templates/images"), name="images")

async def get_data_from_db():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    query = '''
        SELECT * from player_info_view;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


async def get_data_from_db2():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    query = '''
        SELECT dates, event_type, COUNT(*) AS count
    FROM sumuser
    GROUP BY dates, event_type;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

async def get_data_from_db3():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    query = '''
       SELECT DATE_FORMAT(dates, '%Y-%m-%d') as dates,registrate_count,last_login_count from tri_table;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generic", response_class=HTMLResponse)
async def generic(request: Request):
    return templates.TemplateResponse("generic.html", {"request": request})

@app.get("/elements", response_class=HTMLResponse)
async def generic(request: Request):
    return templates.TemplateResponse("elements.html", {"request": request})


@app.websocket("/money_ws") # 1 
async def money_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data_from_db = await get_data_from_db()
        sorted_data = sorted(data_from_db, key=lambda x: x['usermoney'], reverse=True)
        money_data = [{"name": item["name"], "usermoney": item["usermoney"]} for item in sorted_data]  # 전송할 형태로 만든다
        await websocket.send_text(json.dumps(money_data)) # 클라이언트에게 json형식으로 텍스트로 데이터를 전송해줌
        await asyncio.sleep(10)

@app.websocket("/bankmoney_ws")  #2
async def bankmoney_websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 

    while True:
        data_from_db = await get_data_from_db()
        sorted_data = sorted(data_from_db, key=lambda x: x['bankmoney'], reverse=True)
        bank_data = [{"name": item["name"], "bankmoney": item["bankmoney"]} for item in sorted_data]
        await websocket.send_text(json.dumps(bank_data)) #websoket을 통해 클라이언트로 보냄
        await asyncio.sleep(10)

@app.websocket("/level_ws") # 3
async def level_websocket_endpodint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data_from_db = await get_data_from_db()
        sorted_data = sorted(data_from_db, key=lambda x: x['banklevel'], reverse=True)
        level_data = [{"name": item["name"], "level": item["banklevel"]} for item in sorted_data]
        await websocket.send_text(json.dumps(level_data))
        await asyncio.sleep(10)


@app.websocket("/bankmoney2_ws") #4
async def lbankmoney2_websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 

    while True:
        data_from_db = await get_data_from_db()
        level_data = [{"name": item["name"], "bankmoney": item["bankmoney"]} for item in data_from_db]
        await websocket.send_text(json.dumps(level_data)) #websoket을 통해 클라이언트로 보냄
        await asyncio.sleep(10)

@app.websocket("/level2_ws") #5
async def level2_websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 

    while True:
        data_from_db = await get_data_from_db()
        level_data = [{"name": item["name"], "level": item["banklevel"]} for item in data_from_db]
        await websocket.send_text(json.dumps(level_data)) #websoket을 통해 클라이언트로 보냄
        await asyncio.sleep(10)

@app.websocket("/moneylevel_ws") # 6
async def moneylevel_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data_from_db = await get_data_from_db()
        money_data = [
    {
        "name": item["name"],
        "money": item['usermoney'] / (item['usermoney'] + item['bankmoney']) if (item['usermoney'] + item['bankmoney']) != 0 else 1,
        "bankmoney": item['bankmoney'] / (item['usermoney'] + item['bankmoney']) if (item['usermoney'] + item['bankmoney']) != 0 else 1  # 0으로 나누는 것을 피하기 위한 조건 추가
    }
    for item in data_from_db
    ]
        await websocket.send_text(json.dumps(money_data))
        await asyncio.sleep(10)

@app.websocket("/userline_ws")
async def userline_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data_from_db2 = await get_data_from_db2()
        data_from_db3 = await get_data_from_db3()
        await websocket.send_text(json.dumps({'type': 'data_from_db2', 'data': data_from_db2}))
        await websocket.send_text(json.dumps({'type': 'data_from_db3', 'data': data_from_db3}))
        await asyncio.sleep(10)

