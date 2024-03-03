from load import load_all
from user import user_all
from shop import shop_all
from chat import chat_all
from view import plot_all

# 전처리 
df, lst, user_df = load_all()
login_df, time , top_users ,time_df  = user_all()
buy_df , sell_df_multi , sell_df_one , sell_df , buy_item_cost,buy_item_count,buy_item_category,sell_df_multi_cost,sell_df_one_cost,king_user_buy,user_buy_category,user_buy_item,sell_count_data,sell_count_data2,king_user_sell = shop_all()
chat_df,chat_df_new , top_chat,top_chat_new = chat_all()

# 시각화 
plot_all()



# prin(sell_df) 

# groupby를 reset_index하면 dataframe이 되네 ?
# print(top_chat_new)


