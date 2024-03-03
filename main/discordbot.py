import discord
from discord.ext import commands
import mysql.connector
from datetime import datetime

# MySQL 데이터베이스 연결 설정
db_connection = #정보 생략

cursor = db_connection.cursor()

# 봇 설정
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("봇이 실행될때 콘솔창에 뜰 메세지")
    print(bot.user.name)
    print(bot.user.id)
    print('_______________________________________________')

    # 봇이 시작될 때 특정 채널에 메시지
    channel_id = 1198178676093763694  
    channel = bot.get_channel(channel_id)

    if channel:
        current_date = datetime.now().strftime("%Y년 %m월 %d일")
        announcement_message = (
            f'-------<{current_date}>-------\n'
            '안녕하세요! 오늘도 좋은 하루입니다\n'
            '저는 건의사항을 들어주는 Forecity 편지봇입니다.\n'
            '건의사항이 있다면 저에게 DM을 보내주세요!!'
        )
        await channel.send(announcement_message)
    else:
        print(f"채널 ID {channel_id}에 해당하는 채널을 찾을 수 없습니다.")
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # 봇이 보낸 메시지는 무시합니다.

    # 특정 채널에서 온 메시지만 처리
    if message.channel.id == 1198178676093763694:
        # 채널에 온 메시지에 대한 추가 처리가 필요한 경우 여기에 작성합니다.
        pass

    # DM에서 온 메시지만 처리
    elif message.guild is None:
        response = "질문이 접수되었습니다. 빠른 시일내에 답변 드리겠습니다."
        await message.channel.send(response)

        # 메시지를 MySQL 데이터베이스에 저장
        insert_query = "INSERT INTO messages2 (user_id, content) VALUES (%s, %s)"
        insert_data = (str(message.author.id), message.content)
        cursor.execute(insert_query, insert_data)
        db_connection.commit()

    await bot.process_commands(message)

bot.run('token')
