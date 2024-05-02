# 메인 데이터(log) 로드
from common import convert_to_seconds
import glob
import gzip
import re
import pandas as pd
import matplotlib.pyplot as plt

def load_main_data():
    # 옵션 설정
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False
    pd.set_option('display.max.colwidth', 1000)

    pattern = r"\[(.*?)\] \[(.*?)\]: (.*)"
    file_list = glob.glob('log/*.gz')
    data = []
    for file in file_list:
        with gzip.open(file, 'rb') as f:
            log_data = f.read().decode('utf-8')
            groups = re.findall(pattern, log_data)
            for group in groups:
                data.append(group)

    df = pd.DataFrame(data, columns=['Timestamp', 'Level', 'Message'])
    df = df[~df['Message'].str.contains('청소')]  # 청소 관련 처리
    return df

# DB 데이터 로드
def load_db_data():
    import mysql.connector
    import pandas as pd

    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        database="view_dbb"
    )
    cursor = db.cursor()
    query = 'SELECT * FROM player_info_view'
    cursor.execute(query)
    rows = cursor.fetchall()
    user_df = pd.DataFrame(rows, columns=['아이디', '이름', '계좌돈', '은행레벨', '유저돈', '플레이어여부', '등록날짜',
                                          '마지막로그인', '전체게임수(도박)', '승리횟수(도박)',
                                          '작은승리횟수(도박)', '패배횟수(도박)'])
    lst = list(user_df['이름'].values)  # 다른 데이터와 비교를 위해
    return lst, user_df

# 로드 함수 실행
def load_all():
    df = load_main_data()
    lst, user_df = load_db_data()
    return df, lst, user_df

if __name__ == "__main__":
    load_all()


