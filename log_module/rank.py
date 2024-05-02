from load import load_all
from user import user_all
from shop import shop_all
from chat import chat_all
import pandas as pd

df, lst, user_df = load_all()
login_df, time , top_users ,time_df , vip_user = user_all()
buy_df , sell_df_multi , sell_df_one , sell_df , buy_item_cost , buy_item_count , buy_item_category , king_user_buy , vip_buy_user_category , vip_buy_user_item,sell_df_one_cost,sell_count_data,sell_count_data2,king_user_sell,vip_sell_user_category,vip_sell_user_item= shop_all()
chat_df,chat_df_new , top_chat,top_chat_new = chat_all()


def rank_all():
    max_rank=200
    buy_grouped = buy_df.groupby('user')['cost'].sum().reset_index(name='누적 구매 금액')
    sell_grouped = sell_df.groupby('user')['cost'].sum().reset_index(name='누적 판매 금액')

    # 순위 매기기
    buy_grouped['buy_rank'] = buy_grouped['누적 구매 금액'].rank(ascending=False)
    sell_grouped['sell_rank'] = sell_grouped['누적 판매 금액'].rank(ascending=False)
    buy_grouped['buy_score'] = max_rank - buy_grouped['buy_rank'] 
    sell_grouped['sell_score'] = max_rank - sell_grouped['sell_rank'] 

    # shop 순위까지 계산
    merged_df = pd.merge(buy_grouped, sell_grouped, on='user', how='outer').fillna(0)
    merged_df['shop_rank'] = merged_df['buy_rank'] + merged_df['sell_rank']
    merged_df['shop_score'] = max_rank - merged_df['shop_rank'] 
    
    
    # time 순위까지 계산
    m_df = pd.merge(time_df, merged_df, on='user', how='left').fillna(0)
    
    # chat 순위까지 계산
    chatt_df = chat_df[['user','chat']]
    chat_rank_df = pd.DataFrame(chatt_df['user'].value_counts().rank(method='min', ascending=False)).reset_index()
    final_rank_df = pd.merge(m_df, chat_rank_df, on='user', how='left')
    final_rank_df = final_rank_df.rename(columns={'count': 'chat_rank'}).fillna(200)
    final_rank_df['chat_score'] = max_rank - final_rank_df['chat_rank'] 
    
    final_rank_df['final_score'] = final_rank_df['shop_score'] + final_rank_df['chat_score'] + final_rank_df['time_score']
    final_rank_df['final_rank'] = final_rank_df['final_score'].rank(ascending=False, method='min')
    return final_rank_df


if __name__ == "__main__":
    rank_all()
