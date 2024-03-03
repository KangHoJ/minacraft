import discord
from discord.ext import commands
import mysql.connector

# Discord 봇 설정
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

# MySQL 연결 설정
try:
    db = #db정보
    print("Connected to MySQL database successfully!")
except mysql.connector.Error as err:
    print("Error connecting to MySQL database:", err)
cursor = db.cursor()

# Discord 이벤트: 봇이 준비되었을 때 실행
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Discord 명령어: !테이블보여줘 명령을 통해 테이블 내용 표시
@bot.command(name='테이블보여줘')
async def show_table(ctx):
    # MySQL 쿼리 실행
    query = "SELECT * FROM messages2"
    cursor.execute(query)
    print("Executing query:", query)
    rows = cursor.fetchall()
    print("Fetched rows:", rows)
    
    # 결과를 Discord 특정 채널에 전송
    target_channel_id = 1206563500915171358
    target_channel = bot.get_channel(target_channel_id)
    for row in rows:
        await target_channel.send(row)

# Discord 봇 실행
bot.run('toekn')



