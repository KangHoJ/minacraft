from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from io import BytesIO
import base64
import os
import asyncio
app = FastAPI()
os.makedirs('./image', exist_ok=True)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

async def refresh_page():
    while True:
        await asyncio.sleep(10)
    
@app.get("/",response_class=HTMLResponse)
async def read_root(request: Request):
    # 첫 번째 데이터 시각화
    df = pd.read_csv('extracted_data.csv')
    plt.subplot(1, 2, 1)
    plt.bar(df['name'], df['money'])
    plt.xlabel('name')
    plt.ylabel('Value')
    plt.title('user - money')

    # 두 번째 데이터 시각화
    plt.subplot(1, 2, 2)
    plt.bar(df['name'], df['level'])
    plt.xlabel('uuid')
    plt.ylabel('Value')
    plt.title('user id - money')

    # 전체 그림을 이미지로 변환
    image_stream = BytesIO()
    plt.savefig('./image/bar_charts.png', format='png')
    plt.close()

    # 이미지를 Base64로 인코딩
    with open('./image/bar_charts.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    return templates.TemplateResponse("bar.html", {"request": request, "encoded_image": encoded_image})
asyncio.create_task(refresh_page())