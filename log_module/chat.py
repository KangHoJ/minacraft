# 채팅 분석
from common import extract_user_info
from load import load_all

df, lst, user_df = load_all()
def chat_info_fuc():
    global chat_df
    global chat_df_new

    chat_df = df[df['Level'].str.contains('Async Chat Thread')]
    extract_user_info(chat_df,lst) # message에서 유저 생성
    chat_df_new = chat_df[chat_df['Message'].str.contains('[뉴비]')] 
    
    pattern = r">>\s*(.*)" 
    chat_df['chat'] = chat_df['Message'].str.extract(pattern)
    chat_df_new['chat'] = chat_df_new['Message'].str.extract(pattern)
    return chat_df,chat_df_new

def chat_info():
    top_chat = chat_df['user'].value_counts()
    top_chat_new = chat_df_new['user'].value_counts()
    return top_chat,top_chat_new

def chat_all():
    chat_df,chat_df_new = chat_info_fuc()
    top_chat,top_chat_new = chat_info()
    return chat_df,chat_df_new , top_chat,top_chat_new

if __name__ == "__main__":
    chat_all()

    