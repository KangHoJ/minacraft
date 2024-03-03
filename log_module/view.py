import seaborn as sns
import matplotlib.pyplot as plt
from user import user_all
from chat import chat_all
from shop import shop_all

login_df, time , top_users ,time_df  = user_all()
buy_df , sell_df_multi , sell_df_one , sell_df , buy_item_cost,buy_item_count,buy_item_category,sell_df_multi_cost,sell_df_one_cost,king_user_buy,user_buy_category,user_buy_item,sell_count_data,sell_count_data2,king_user_sell = shop_all()
chat_df,chat_df_new , top_chat,top_chat_new = chat_all()


def plot_time_chat():
    fig, axs = plt.subplots(2, 2, figsize=(30, 8))

    sns.barplot(x=top_users.index, y=top_users.values, ax=axs[0,0], color="skyblue")
    axs[0,0].set_title("접속 순위")
    axs[0,0].set_xlabel("유저 이름")
    axs[0,0].set_ylabel("접속 횟수")


    sns.barplot(x=time_df['User'], y=time_df['누적 시간'], ax=axs[0,1], color="tomato")
    axs[0,1].set_title("누적 시간 순위")
    axs[0,1].set_xlabel("유저 이름")
    axs[0,1].set_ylabel("누적 시간")

    sns.barplot(x=top_chat.index, y=top_chat.values, ax=axs[1,0], color="skyblue")
    axs[1,0].set_title("채팅 순위(전체)")
    axs[1,0].set_xlabel("유저 이름")
    axs[1,0].set_ylabel("채팅 횟수(전체)")


    sns.barplot(x=top_chat_new.index, y=top_chat_new.values, ax=axs[1,1], color="tomato")
    axs[1,1].set_title("채팅 순위(뉴비)")
    axs[1,1].set_xlabel("유저 이름")
    axs[1,1].set_ylabel("채팅 횟수(뉴비)")

    plt.subplots_adjust(left=0.05, right=0.95 , hspace=0.475 , wspace=0.13)
    plt.suptitle("접속 왕 / 누적 시간 왕", fontsize=16, y=1.05 , ha="center")
    plt.savefig('time_chat.png')
    plt.show()    
    plt.close()

def plot_buy():
    fig, axs = plt.subplots(2, 3, figsize=(30, 8))

    sns.barplot(x=buy_item_cost.index, y=buy_item_cost.values, ax=axs[0,0], color="skyblue")
    axs[0,0].set_title("산 금액이 높은 아이템")
    axs[0,0].set_xlabel("아이템")
    axs[0,0].set_ylabel("총 비용")


    sns.barplot(x=buy_item_count.index, y=buy_item_count.values, ax=axs[0,1], color="tomato")
    axs[0,1].set_title("가장 많이 산 아이템")
    axs[0,1].set_xlabel("아이템")
    axs[0,1].set_ylabel("개수")

    sns.barplot(x=buy_item_category.index, y=buy_item_category.values, ax=axs[0,2], color="tomato")
    axs[0,2].set_title("가장 많이 산 카테고리")
    axs[0,2].set_xlabel("카테고리")
    axs[0,2].set_ylabel("개수")


    sns.barplot(x=king_user_buy.index, y=king_user_buy.values, ax=axs[1,0], color="skyblue")
    axs[1,0].set_title("유저 구매왕")
    axs[1,0].set_xlabel("유저 이름")
    axs[1,0].set_ylabel("구매 개수")

    user_buy_category_df = user_buy_category.reset_index() 
    sns.barplot(x='user', y='Count', hue='category', ax=axs[1,1] , data=user_buy_category_df,color="skyblue")
    axs[1,1].set_title("유저별 많이 산 카테고리")
    axs[1,1].set_xlabel("유저 이름")
    axs[1,1].set_ylabel("카테고리 개수")

    user_buy_item_df = user_buy_item.reset_index()
    sns.barplot(x='user', y='Count', hue='Item', ax=axs[1,2] , data=user_buy_item_df,color="skyblue")
    axs[1,2].set_title("유저별 많이 산 아이템")
    axs[1,2].set_xlabel("유저 이름")
    axs[1,2].set_ylabel("아이템 개수")


    plt.subplots_adjust(left=0.05, right=0.95 , hspace=0.475 )
    plt.suptitle("접속 왕 / 누적 시간 왕", fontsize=16, y=1.05 , ha="center")
    plt.savefig('buy.png')
    plt.show()
    plt.close()

def plot_sell():
    fig, axs = plt.subplots(3, 2, figsize=(30, 10))

    sns.barplot(x=sell_df_multi_cost.index, y=sell_df_multi_cost.values, ax=axs[0,0], color="skyblue")
    axs[0,0].set_title("판매(조합) 돈번 조합 순위 ")
    axs[0,0].set_xlabel("아이템")
    axs[0,0].set_ylabel("총 비용")


    sns.barplot(x=sell_df_one_cost.index, y=sell_df_one_cost.values, ax=axs[0,1], color="tomato")
    axs[0,1].set_title("판매(단일) 돈번 조합 순위")
    axs[0,1].set_xlabel("아이템")
    axs[0,1].set_ylabel("개수")

    sns.barplot(x='품목', y='판매량', ax=axs[1,0] , data=sell_count_data,color="skyblue")
    axs[1,0].set_title("가장 많이 판 아이템")
    axs[1,0].set_xlabel("아이템")
    axs[1,0].set_ylabel("개수")


    sns.barplot(x='카테고리', y='판매량', ax=axs[1,1] , data=sell_count_data2,color="skyblue")
    axs[1,1].set_title("가장 많이 판 카테고리")
    axs[1,1].set_xlabel("아이템")
    axs[1,1].set_ylabel("카테고리")


    king_user_sell_df = king_user_sell.reset_index() 
    sns.barplot(x='user', y='cost', ax=axs[2,0] , data=king_user_sell_df,color="skyblue")
    axs[2,0].set_title("유저 판매왕")
    axs[2,0].set_xlabel("유저 이름")
    axs[2,0].set_ylabel("판매 금액")

    # 추후 업데이트 ! 
    # user_buy_item_df = user_buy_item.reset_index()
    # sns.barplot(x='user', y='Count', hue='Item', ax=axs[1,2] , data=user_buy_item_df,color="skyblue")
    # axs[1,2].set_title("유저별 많이 산 아이템")
    # axs[1,2].set_xlabel("유저 이름")
    # axs[1,2].set_ylabel("아이템 개수")


    plt.subplots_adjust(left=0.05, right=0.95 , hspace=0.475 )
    plt.suptitle("접속 왕 / 누적 시간 왕", fontsize=16, y=1.05 , ha="center")
    plt.savefig('sell.png')
    plt.show()    
    plt.close


def plot_all():
    plot_time_chat()
    plot_buy()
    plot_sell()


if __name__ == "__main__":
    plot_all()


