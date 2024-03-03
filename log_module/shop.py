from common import extract_user_info
from load import load_all
from user import user_all
from collections import Counter
import pandas as pd

df, lst, user_df = load_all()
login_df, time, top_users, time_df = user_all()

# 구입분석 
def buy_df_func():
    buy_df = df[df['Message'].str.contains('구입')].copy()
    buy_df['Item'] = buy_df['Message'].str.extract(r'님이 ([^(]+)') # 님이 이후에 괄호를 뺀 모든 문자열 (아이템명)
    buy_df['Count'] = buy_df['Message'].str.extract(r'(\d+) 만큼') # 만큼 전 숫자 (몇개 샀는지)
    buy_df['cost'] = buy_df['Message'].str.extract(r'(\d+)를') # 를 전 숫자 (총 얼마인지) 
    buy_df["category"] = buy_df["Message"].str.findall(r"\((.+?)\.") # 몇개 샀는지 
    buy_df["category"] = buy_df["category"].apply(lambda x: ', '.join(x))
    buy_df = buy_df.astype({'Count': int, 'cost': int})
    buy_df = buy_df.reset_index().drop('index',axis=1)
    extract_user_info(buy_df,lst) # 유저 만 추출 
    return buy_df


def sell_df_multi_func(): # 한번에 여러상품 판경우
    sell_df_multi = df[df['Message'].str.contains('판매 gui')]
    sell_df_multi = sell_df_multi[~sell_df_multi['Message'].str.contains('챗')] # 이상치 제거 
    sell_df_multi['item'] = sell_df_multi['Message'].str.extractall(r'(\d+x\s([\w\s]+)\(.*?\))')[1].groupby(level=0).apply(list) # 여러개일수도 있으므로(아이템명)
    sell_df_multi['item'] = sell_df_multi['item'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x) 
    sell_df_multi['cost'] = sell_df_multi['Message'].str.extract(r'for (\d{1,3}(?:,\d{3})*(?:\.\d+)?)') # 총 비용 
    sell_df_multi['cost'] = sell_df_multi['cost'].str.replace(',', '').astype(float)
    sell_df_multi["category"] = sell_df_multi["Message"].str.findall(r"\((.+?)\.") # 카테고리 
    sell_df_multi["category"] = sell_df_multi["category"].apply(lambda x: ', '.join(x)) # 여러개일수도 있으므로
    sell_df_multi = sell_df_multi.reset_index().drop('index',axis=1)
    return sell_df_multi


def sell_df_one_func(): # 한번에 한종류 상품 판경우
    sell_df_one = df[df['Message'].str.contains('판매 하셨습니다')].copy()
    sell_df_one['item'] = sell_df_one['Message'].str.extract(r'님이 ([^(]+)') # 아이템명 
    sell_df_one['cost'] = sell_df_one['Message'].str.extract(r'(\d+)를') # 총 얼마인지 
    sell_df_one['cost'] = sell_df_one['cost'].astype(float) 
    sell_df_one["category"] = sell_df_one["Message"].str.findall(r"\((.+?)\.") # 카테고리 
    sell_df_one["category"] = sell_df_one["category"].apply(lambda x: ', '.join(x)) # 여러개일수도 있으므로
    sell_df_one = sell_df_one.reset_index().drop('index',axis=1)
    return sell_df_one

''' 참고로 한개 판 경우 count를 만들지 않은 이유는 여러개 여러개판경우와 합치기 위해서다. 
    나중에 counter함수를 이용해 물품별 판매 갯수를 충분히 셀 수 있다! 구매는 하나를 산 경우만 있으므로 따로 count를 만들어줌 '''


def shop_all_func():
    global buy_df
    global sell_df_multi
    global sell_df_one
    global sell_df

    buy_df = buy_df_func()
    sell_df_multi = sell_df_multi_func()
    sell_df_one = sell_df_one_func()
    sell_df = pd.concat([sell_df_multi,sell_df_one])
    sell_df['item'] = sell_df['item'].str.replace(',\s*', ',', regex=True) # 공백제거
    sell_df['category'] = sell_df['category'].str.replace(',\s*', ',', regex=True) #공백제거
    extract_user_info(sell_df,lst)

    return buy_df , sell_df_multi , sell_df_one , sell_df


def shop_info():
    buy_item_cost = buy_df.groupby('Item')['cost'].sum().sort_values(ascending=False).head(5) # 가장 산금액이 높은 아이템 
    buy_item_count = buy_df.groupby('Item')['Count'].sum().sort_values(ascending=False).head(5) # 가장 많이 산 아이템
    buy_item_category = buy_df.groupby('category')['Count'].sum().sort_values(ascending=False).head(5) # 가장 많이 산 카테고리

    king_user_buy = buy_df.groupby('user')['Count'].sum().sort_values(ascending=False).head(5) # 유저 구매왕
    user_buy_category = buy_df.groupby(['user','category'])['Count'].sum().sort_values(ascending=False).head(5) # 유저별 카테고리 구매 개수 
    user_buy_item = buy_df.groupby(['user','Item'])['Count'].sum().sort_values(ascending=False).head(7) # 유저별 어떤 아이템 많이 샀는지 

    sell_df_multi_cost = sell_df_multi.groupby('item')['cost'].sum().sort_values(ascending=False).head(3)  # 조합 최고 돈번 상품 
    sell_df_one_cost = sell_df_one.groupby('item')['cost'].sum().sort_values(ascending=False).head(5) # 한개만 캐서 파는 최고 돈번 상품 


    all_words = ",".join(sell_df["item"])
    word_counts = Counter(all_words.split(','))
    sell_count =  word_counts.most_common(7)
    sell_count_data = pd.DataFrame(sell_count, columns=['품목', '판매량']) # 가장 많이 판매한 아이템 


    all_words2 = ",".join(sell_df["category"])
    word_counts2 = Counter(all_words2.split(','))
    sell_count2 =  word_counts2.most_common(10)
    sell_count_data2 = pd.DataFrame(sell_count2, columns=['카테고리', '판매량']) # 가장 많이 판매한 카테고리 

    
    king_user_sell = sell_df.groupby('user')['cost'].sum().sort_values(ascending=False).head(5) # 유저 판매왕

    return buy_item_cost,buy_item_count,buy_item_category,sell_df_multi_cost,sell_df_one_cost,king_user_buy,user_buy_category,user_buy_item,sell_count_data,sell_count_data2,king_user_sell


def shop_all():
    buy_df , sell_df_multi , sell_df_one , sell_df = shop_all_func()
    buy_item_cost,buy_item_count,buy_item_category,sell_df_multi_cost,sell_df_one_cost,king_user_buy,user_buy_category,user_buy_item,sell_count_data,sell_count_data2,king_user_sell = shop_info()

    return  buy_df , sell_df_multi , sell_df_one , sell_df , buy_item_cost,buy_item_count,buy_item_category,sell_df_multi_cost,sell_df_one_cost,king_user_buy,user_buy_category,user_buy_item,sell_count_data,sell_count_data2,king_user_sell 


if __name__ == "__main__":
    shop_all()