# 메시지에서 유저 정보 추출
def extract_user_info(df, lst):
    extracted = []
    for message in df['Message']:
        for ltem in lst:
            if ltem in message:
                extracted.append(ltem)
                break
        else:
            extracted.append(' ')
    df['user'] = extracted
    return df

# timestamp를 초로 변환
def convert_to_seconds(timestamp):
    import datetime
    time_obj = datetime.datetime.strptime(timestamp, '%H:%M:%S')
    seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    # 새벽 시간 (00:00:00 ~ 06:00:00) 처리
    if time_obj.hour < 6:
        seconds += 86400
    return seconds
