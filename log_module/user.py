from common import convert_to_seconds
import pandas as pd
from load import load_all
df, lst, user_df = load_all()



def login_df_func():
    global login_df
    login_df = df[(df['Message'].str.contains('\[\+\].*')) | (df['Message'].str.contains('\[\-\].*'))] # 입,출입만
    login_df = login_df[~login_df['Message'].str.contains('님이')].reset_index().drop(['index'],axis=1) # 전처리
    login_df = login_df.drop([0, 2, 610])  # 이상 데이터 전처리 
    login_df['Seconds'] = login_df['Timestamp'].apply(convert_to_seconds) # 시간변환 
    return login_df

def time_df_func():
    global time
    time =[]
    for li in lst:
        plus = []
        minus = []
        for idx, message in enumerate(login_df['Message']):
            if (li in message) and ('[+]' in message):
                plus.append(login_df.iloc[idx]['Seconds'])
            elif (li in message) and ('[-]' in message):
                minus.append(login_df.iloc[idx]['Seconds'])

        # [+] 개수와 [-] 개수가 같은지 확인
        if len(plus) == len(minus):
            total_plus_time = sum(plus)
            total_minus_time = sum(minus)
            result = total_minus_time - total_plus_time
            time.append(result/3600)
        else:
            print(f"사용자 '{li}'의 [+] 개수와 [-] 개수가 일치하지 않습니다. plus 개수 : {len(plus)} , minus 개수 : {len(minus)}")
    return time

def user_info():
    top_users = login_df['Message'].str.extract(r'\[\w+\] ?(\w+)')[0].value_counts().head(5) # 지표1. 유저 로그인 순위 series
    time_df = pd.DataFrame({'User': lst , '누적 시간': time}).sort_values(by='누적 시간',ascending=False).reset_index().drop('index',axis=1).head(10) # 지표 2. 유저별 누적시간 순위 데이터  
    return top_users , time_df

def user_all():
    login_df = login_df_func() 
    time = time_df_func()  
    top_users , time_df = user_info()  
    return login_df, time , top_users ,time_df 


# 유저 접속 순위 / 유저 접속 시간 순위
if __name__ == "__main__":
    user_all()
    # print(len(time))
    # print(len(lst))