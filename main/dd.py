import discord
from discord.ext import commands, tasks
import mysql.connector
from datetime import timedelta
import datetime

# Discord 봇 설정
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())


# MySQL 연결 설정
@tasks.loop(minutes=60)
async def loop_task():
    try:
        db = # 정보 입력 생략
        print("연결 성공!")
    except mysql.connector.Error as err:
        print("MYSQL 연결 에러:", err)

    cursor = db.cursor()
    query2 = 'SELECT content FROM messages2'
    cursor.execute(query2)
    rows2 = cursor.fetchall()
    print('db정보',rows2)
    now = datetime.datetime.now()
    print('현재시간:',now)
    last_executed_time = now - timedelta(minutes=61)
    print('비교시간:',last_executed_time)
    query = f"SELECT * FROM messages2 WHERE created_at > '{last_executed_time}'"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        # 새로운 row가 있다면 채널에 전송
        target_channel_id = 1206563500915171358
        target_channel = bot.get_channel(target_channel_id)
        for row in rows:
            await target_channel.send(row)

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        print("쿼리 에러:", err)


@bot.command(name='전체테이블보여줘')
async def show_all_table(ctx):
    try:
        db2 = #정보 생략
        print("연결 성공!")
    except mysql.connector.Error as err:
        print("MYSQL 연결 에러:", err)

    query = "SELECT * FROM messages2"
    cursor2 = db2.cursor()
    cursor2.execute(query)
    rows = cursor2.fetchall()

    target_channel_id = 1206563500915171358
    target_channel = bot.get_channel(target_channel_id)
    for row in rows:
        await target_channel.send(row)

    cursor2.close()
    db2.close()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    loop_task.start() # loop_task 함수 실행 시작

# Discord 봇 실행
bot.run('token')
