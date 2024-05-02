from load import load_all
from user import user_all
from shop import shop_all
from chat import chat_all
from view import plot_all
from rank import rank_all

# 전처리 
df, lst, user_df = load_all()
login_df, time , top_users ,time_df , vip_user = user_all()
buy_df , sell_df_multi , sell_df_one , sell_df , buy_item_cost , buy_item_count , buy_item_category , king_user_buy , vip_buy_user_category , vip_buy_user_item,sell_df_one_cost,sell_count_data,sell_count_data2,king_user_sell,vip_sell_user_category,vip_sell_user_item = shop_all()
chat_df,chat_df_new , top_chat,top_chat_new = chat_all()
final_rank_df = rank_all()


# 시각화 
plot_all()



# prin(sell_df) 

# groupby를 reset_index하면 dataframe이 되네 ?
# print(top_chat_new)


