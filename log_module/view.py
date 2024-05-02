import seaborn as sns
import matplotlib.pyplot as plt
from user import user_all
from chat import chat_all
from shop import shop_all
from rank import rank_all

login_df, time , top_users ,time_df , vip_user= user_all()
buy_df , sell_df_multi , sell_df_one , sell_df , buy_item_cost , buy_item_count , buy_item_category , king_user_buy , vip_buy_user_category , vip_buy_user_item,sell_df_one_cost,sell_count_data,sell_count_data2,king_user_sell,vip_sell_user_category,vip_sell_user_item= shop_all()
chat_df,chat_df_new , top_chat,top_chat_new = chat_all()
final_rank_df = rank_all()


def plot_time_user():
    fig, axs = plt.subplots(3, 1, figsize=(15, 15))
    
    # 1. 유저별 접속 횟수 및 누적 시간 
    top_usercount_rank = top_users.head(10)
    axs[0].plot(top_usercount_rank.index, top_usercount_rank.values, color="steelblue", marker='o', label='Connection Count')
    axs[0].set_xlabel("유저 이름")
    axs[0].set_ylabel("접속 횟수", color="steelblue")
    axs[0].tick_params(axis='y', labelcolor="steelblue")
    axs[0].set_title("유저별 접속 횟수 및 누적 시간")

    ax2 = axs[0].twinx()
    top_usertime_rank = time_df.head(10)
    ax2.bar(top_usertime_rank['user'], top_usertime_rank['누적 시간'], color='orange', alpha=0.7, label='Cumulative Time')
    ax2.set_ylabel("누적 시간", color="orange")
    ax2.tick_params(axis='y', labelcolor="orange")
    axs[0].legend(['접속 횟수', '누적 시간'], loc='upper right')

    # 2. 유저별 채팅 순위
    top_chat_rank = top_chat.head(5)
    sns.barplot(x=top_chat_rank.index, y=top_chat_rank.values, ax=axs[1], color="skyblue")
    axs[1].set_title("채팅 순위(전체)")
    axs[1].set_ylabel("채팅 횟수(전체)")

    # 3. 뉴비 유저 채팅 순위
    top_chat_rank_new = top_chat_new.head(5)
    sns.barplot(x=top_chat_rank_new.index, y=top_chat_rank_new.values, ax=axs[2], color="tomato")
    axs[2].set_title("채팅 순위(뉴비)")
    axs[2].set_ylabel("채팅 횟수(뉴비)")

    plt.subplots_adjust(left=0.05, right=0.95, hspace=0.475)
    plt.suptitle("접속 왕 / 누적 시간 왕", fontsize=16, y=1.05, ha="center")
    plt.savefig('1.png')
    plt.show()
    plt.close()

def plot_buy():
    fig, axs = plt.subplots(2, 3, figsize=(30, 8))

    # 1.가장 산금액이 높은 아이템 
    sns.barplot(x=buy_item_cost.index, y=buy_item_cost.values, ax=axs[0,0], color="tomato")
    axs[0,0].set_title("산 금액이 높은 아이템")
    axs[0,0].set_xlabel("아이템")
    axs[0,0].set_ylabel("총 비용")

    # 2.가장 많이 산 아이템
    sns.barplot(x=buy_item_count.index, y=buy_item_count.values, ax=axs[0,1], color="tomato")
    axs[0,1].set_title("가장 많이 산 아이템")
    axs[0,1].set_xlabel("아이템")
    axs[0,1].set_ylabel("개수")

    # 3.가장 많이 산 카테고리
    sns.barplot(x=buy_item_category.index, y=buy_item_category.values, ax=axs[0,2], color="tomato")
    axs[0,2].set_title("가장 많이 산 카테고리")
    axs[0,2].set_xlabel("카테고리")
    axs[0,2].set_ylabel("개수")

    # 4.유저 구매왕
    sns.barplot(x=king_user_buy.index, y=king_user_buy.values, ax=axs[1,0], color="skyblue")
    axs[1,0].set_title("유저 구매왕")
    axs[1,0].set_xlabel("유저 이름")
    axs[1,0].set_ylabel("구매 개수")

    # 5.vip 유저 카테고리별 구매
    user_buy_category_df = vip_buy_user_category.reset_index().head(10)
    sns.barplot(x='user', y='Count', hue='category', ax=axs[1,1] , data=user_buy_category_df,palette="pastel")
    axs[1,1].set_title("vip 유저별 많이 산 카테고리")
    axs[1,1].set_xlabel("유저 이름")
    axs[1,1].set_ylabel("카테고리 개수")

    # 6.vip 유저별 가장 많이 산 아이템
    user_buy_item_df = vip_buy_user_item.reset_index().head(10)
    sns.barplot(x='user', y='Count', hue='Item', ax=axs[1,2] , data=user_buy_item_df,palette="pastel")
    axs[1,2].set_title("vip 유저별 많이 산 아이템")
    axs[1,2].set_xlabel("유저 이름")
    axs[1,2].set_ylabel("아이템 개수")


    plt.subplots_adjust(left=0.05, right=0.95 , hspace=0.475 )
    plt.suptitle("접속 왕 / 누적 시간 왕", fontsize=16, y=1.05 , ha="center")
    plt.savefig('2.png')
    plt.show()
    plt.close()

def plot_sell():
    fig, axs = plt.subplots(2, 3, figsize=(30, 10))

    # sns.barplot(x=sell_df_multi_cost.index, y=sell_df_multi_cost.values, ax=axs[0,0], color="skyblue")
    # axs[0,0].set_title("판매(조합) 돈번 조합 순위 ")
    # axs[0,0].set_xlabel("아이템")
    # axs[0,0].set_ylabel("총 비용")


    # 7.한개만 캐서 파는 최고 돈번 상품 
    sns.barplot(x=sell_df_one_cost.index, y=sell_df_one_cost.values, ax=axs[0,0], color="tomato")
    axs[0,0].set_title("판매(단일) 돈번 조합 순위")
    axs[0,0].set_xlabel("아이템")
    axs[0,0].set_ylabel("개수")

    # 8.가장 많이 판매한 아이템 
    sns.barplot(x='품목', y='판매량', ax=axs[0,1] , data=sell_count_data,color="tomato")
    axs[0,1].set_title("가장 많이 판 아이템")
    axs[0,1].set_xlabel("아이템")
    axs[0,1].set_ylabel("개수")

    # 9.가장 많이 판매한 카테고리 
    sns.barplot(x='카테고리', y='판매량', ax=axs[0,2] , data=sell_count_data2,color="tomato")
    axs[0,2].set_title("가장 많이 판 카테고리")
    axs[0,2].set_xlabel("아이템")
    axs[0,2].set_ylabel("카테고리")

    # 10.유저 판매왕
    king_user_sell_df = king_user_sell.reset_index() 
    sns.barplot(x='user', y='cost', ax=axs[1,0] , data=king_user_sell_df,color="skyblue")
    axs[1,0].set_title("유저 판매왕")
    axs[1,0].set_xlabel("유저 이름")
    axs[1,0].set_ylabel("판매 금액")
    
    # 11. vip 유저 돈 많이 번 카테고리
    vip_sell_user_category_df = vip_sell_user_category.reset_index().head(10)
    sns.barplot(x='user', y='cost', hue='category', ax=axs[1,1] , data=vip_sell_user_category_df,palette="pastel")
    axs[1,1].set_title("vip 유저 돈 번 카테고리 순위")
    axs[1,1].set_xlabel("유저 이름")
    axs[1,1].set_ylabel("판매 금액")
    
    # 12 vip 유저 돈 많이 번 아이템
    vip_sell_user_item_df = vip_sell_user_item.reset_index().head(10)
    sns.barplot(x='user', y='cost', hue='item', ax=axs[1,2] , data=vip_sell_user_item_df,palette="pastel")
    axs[1,2].set_title("vip 유저 돈 번 아이템 순위")
    axs[1,2].set_xlabel("유저 이름")
    axs[1,2].set_ylabel("판매 금액")

    plt.subplots_adjust(left=0.05, right=0.95 , hspace=0.475 )
    plt.suptitle("접속 왕 / 누적 시간 왕", fontsize=16, y=1.05 , ha="center")
    plt.savefig('3.png')
    plt.show()    
    plt.close

def plot_rank():
    fig, axs = plt.subplots(2, 2, figsize=(40, 8))
    top_5_time_ranks = final_rank_df.nlargest(5, 'time_score')
    sns.barplot(x='user', y='time_score', data=top_5_time_ranks, ax=axs[0, 0], color='skyblue')
    axs[0,0].set_title("누적 시간 점수 순위")
    axs[0,0].set_ylabel("누적 접속 시간 점수")
    axs[0, 0].set_ylim(180, 200) 

    top_5_shop_ranks = final_rank_df.nlargest(5, 'shop_score')
    sns.barplot(x='user', y='shop_score', data=top_5_shop_ranks, ax=axs[0, 1], color='lightgreen')
    axs[0,1].set_title("구/판매 금액 점수 순위")
    axs[0,1].set_ylabel("누적 구/판매 금액 점수")
    axs[0,1].set_ylim(180, 200) 

    top_5_chat_ranks = final_rank_df.nlargest(5, 'chat_score')
    sns.barplot(x='user', y='chat_score', data=top_5_chat_ranks, ax=axs[1, 0], color='salmon')
    axs[1,0].set_title("누적 채팅 점수 순위")
    axs[1,0].set_ylabel("누적 채팅 횟수 점수")
    axs[1,0].set_ylim(180, 200) 

    top_5_fianl_ranks = final_rank_df.nlargest(5, 'final_score')
    sns.barplot(x='user', y='final_score', data=top_5_fianl_ranks, ax=axs[1, 1], color='gold')
    axs[1,1].set_title("최종 점수 순위")
    axs[1,1].set_ylabel("최종 점수")
    axs[1,1].set_ylim(550, 600) 
    plt.savefig('4.png')
    plt.show()    
    plt.close()

def plot_all():
    plot_time_user()
    plot_buy()
    plot_sell()
    plot_rank()


if __name__ == "__main__":
    plot_all()


