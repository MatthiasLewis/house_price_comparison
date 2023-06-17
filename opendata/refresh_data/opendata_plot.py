import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import plotly.express as px

#將資料庫內容導入
engine = create_engine("sqlite:///data.db?charset=utf8")
#engine = create_engine("mysql+pymysql://username:password@localhost/databsename?charset=utf8")
df_Wenshan = pd.read_sql("opendata_Wenshan",engine)
df_Xindia = pd.read_sql("opendata_Xindia",engine)

#新增區域欄位
df_Wenshan["區域"]="文山區"
df_Xindia["區域"]="新店區"

# 找到房價最高的前5%資料
threshold = df_Xindia["square_price(萬/坪)"].quantile(0.97)
threshold_low = df_Xindia["square_price(萬/坪)"].quantile(0.05)

df_to_delete = df_Xindia[df_Xindia["square_price(萬/坪)"] > threshold]
df_to_delete_low = df_Xindia[df_Xindia["square_price(萬/坪)"] < threshold_low]
# 從原始 DataFrame 中刪除找到的資料
df_Xindia = df_Xindia.drop(df_to_delete.index)
df_Xindia = df_Xindia.drop(df_to_delete_low.index)

# 找到房價最高的前5%資料
threshold = df_Wenshan["square_price(萬/坪)"].quantile(0.97)
threshold_low = df_Wenshan["square_price(萬/坪)"].quantile(0.05)

df_to_delete = df_Wenshan[df_Wenshan["square_price(萬/坪)"] > threshold]
df_to_delete_low = df_Wenshan[df_Wenshan["square_price(萬/坪)"] < threshold_low]
# 從原始 DataFrame 中刪除找到的資料
df_Wenshan = df_Wenshan.drop(df_to_delete.index)
df_Wenshan = df_Wenshan.drop(df_to_delete_low.index)

drop_type_Xindia = df_Xindia[df_Xindia["type"]=="透天厝"]
drop_type_Wenshan = df_Wenshan[df_Wenshan["type"]=="透天厝"]

df_Wenshan = df_Wenshan.drop(drop_type_Wenshan.index)
df_Xindia = df_Xindia.drop(drop_type_Xindia.index)
# print(df_Xindia.shape)
# print(df_Wenshan.shape)

#合併2個dataframe
df = pd.concat([df_Xindia, df_Wenshan])


def totalyear_avg_houseprice(data1):
    #複製dataframe來進行操作
    df = data1.copy()
    # 將日期欄位轉換成年份欄位
    df['年份'] = pd.to_datetime(df['date']).dt.year
    # 計算每年的平均房價，並設為索引
    average_prices = df.groupby(['年份', '區域', 'type'])['square_price(萬/坪)'].mean().reset_index()

    # 繪製長條圖
    bar_chart = px.bar(average_prices, x='年份', y='square_price(萬/坪)', color='區域', barmode='group', facet_col='type', \
                       title='每年平均房價長條圖')
    bar_chart.update_layout(
    yaxis_title="房價(萬/坪)"
)
    
    # 加入篩選器元件
    def update_layout(fig,x):
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            label="全部",
                            method="update",
                            args=[{"visible": [True, True, True,True, True, True,True]},
                                {"title": f"每年平均房價{x}圖 - 全部"}]
                        ),
                        dict(
                            label="文山區",
                            method="update",
                            args=[{"visible": [True, True, True,False, False, False]},
                                {"title": f"每年平均房價{x}圖 - 文山區"}]
                        ),
                        dict(
                            label="新店區",
                            method="update",
                            args=[{"visible": [False, False, False,True, True,True]},
                                {"title": f"每年平均房價{x}圖 - 新店區"}]
                        ),
                    ]),
                    direction="down",
                    showactive=True,
                    x=0.8,
                    xanchor="center",
                    y=1.2,
                    yanchor="top"
                ),
            ]
        )
        fig.update_yaxes(range=[0, 40])  # 設定 y 軸的範圍，例如 0 到 50

    # update_layout(line_chart,"折線")
    update_layout(bar_chart,"長條")
    
    # line_chart.show()
    bar_chart.show()
    # # 生成HTML文件
    # line_chart.write_html('line_chart.html')
    bar_chart.write_html('bar_totalyearprice.html')




def year_avg_houseprice(data1,year,dis):
    #複製dataframe來進行操作
    df = data1.copy()
    # 將日期欄位轉換成欄位
    df['年份'] = pd.to_datetime(df['date']).dt.year
    df["月份"] = pd.to_datetime(df['date']).dt.month

    # average_prices = df.loc[(df["年份"]==int(year)) & (df["區域"]==f"{dis}")].groupby(["年份",'月份','type'])['square_price(萬/坪)'].mean().reset_index()
    #創每日平均房價及其群組
    daily_avg_prices = df.loc[(df["年份"]==int(year)) & (df["區域"]==f"{dis}")].copy()
    daily_avg_prices["日期"] = pd.to_datetime(daily_avg_prices["date"])
    daily_avg_prices = daily_avg_prices.groupby(["日期", "type"])['square_price(萬/坪)'].mean().reset_index()   

    # 繪製折線圖
    line_chart = px.line(daily_avg_prices, x='日期', y='square_price(萬/坪)',  color='type', line_group='type',title=f'{year}年{dis}每日單坪房價趨勢圖')
    line_chart.update_layout(
    yaxis_title="房價(萬/坪)",
    xaxis_title=f"{year}"
)


    # 加入篩選器元件
    def update_layout(fig,x):
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            label="全部",
                            method="update",
                            args=[{"visible": [True, True, True]},
                                {"title": f"{year}年{dis}每日單坪房價趨勢圖 - 全部"}]
                        ),
                        dict(
                            label="華廈",
                            method="update",
                            args=[{"visible": [True, False, False]},
                                {"title": f"{year}年{dis}每日單坪房價趨勢圖 - 華廈"}]
                        ),
                        dict(
                            label="公寓",
                            method="update",
                            args=[{"visible": [False, False, True]},
                                {"title": f"{year}年{dis}每日單坪房價趨勢圖 - 公寓"}]
                        ),
                        dict(
                            label="住宅大樓",
                            method="update",
                            args=[{"visible": [False, True, False]},
                                {"title": f"{year}年{dis}每日單坪房價趨勢圖 - 住宅大樓"}]
                        ),
                    ]),
                    direction="down",
                    showactive=True,
                    x=0.8,
                    xanchor="center",
                    y=1.2,
                    yanchor="top"
                ),
            ]
        )

        fig.update_yaxes(range=[5, 60])  # 設定 y 軸的範圍，例如 0 到 50
        # fig.update_xaxes(range=[1, 12])  # 設定 x 軸的範圍，例如 0 到 50

    update_layout(line_chart,"折線")

    line_chart.show()
    # 生成HTML文件
    line_chart.write_html(f'line_yearprice_{dis}_{year}.html')



def age_avg_houseprice(data1,dis):
    #複製dataframe來進行操作
    df = data1.copy()
    # 將日期欄位轉換成年份欄位
    df['年份'] = pd.to_datetime(df['date']).dt.year

    #創屋齡group欄位
    # 將 age 在小於等於 10 的設為 "0-10"
    df["屋齡"] = np.where(df["age"] <= 10, "0-10年", "")
    # 將 age 在大於 10 且小於 20 的設為 "10-20"
    df.loc[(df["age"] > 10) & (df["age"] <= 20), "屋齡"] = "10-20年"
    df.loc[(df["age"] > 20) & (df["age"] <= 30), "屋齡"] = "20-30年"
    df.loc[(df["age"] > 30) , "屋齡"] = "30年以上"

    #計算每年的平均房價，並設為索引
    average_prices = df.loc[(df["區域"]==f"{dis}")].groupby(['年份', 'type', "屋齡"])['square_price(萬/坪)'].mean().reset_index()

    # 繪製長條圖
    bar_chart = px.bar(average_prices, x='年份', y='square_price(萬/坪)', color='type', barmode='group', facet_col="屋齡", \
                    title=f'{dis}各屋齡房價長條圖')
    bar_chart.update_layout(
    yaxis_title="房價(萬/坪)"
)
   
    # 加入篩選器元件
    def update_layout(fig,x):
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            label="全部",
                            method="update",
                            args=[{"visible": [True, True, True,True, True, True,True]},
                                {"title": f"{dis}各屋齡房價{x}圖 - 全部"}]
                        ),
                        dict(
                            label="華廈",
                            method="update",
                            args=[{"visible":  [False, False, False,False,False, False, False,False,True,True,True,True]},
                                {"title": f"{dis}各屋齡房價{x}圖 - 華廈"}]
                        ),
                        dict(
                            label="公寓",
                            method="update",
                            args=[{"visible": [False, False, False,False,True, True, True,True,False,False]},
                                {"title": f"{dis}各屋齡房價{x}圖 - 公寓"}]
                        ),
                        dict(
                            label="住宅大樓",
                            method="update",
                            args=[{"visible": [True, True, True,True,False, False, False,False,False,False,False,False]},
                                {"title": f"{dis}各屋齡房價{x}圖 - 住宅大樓"}]
                        ),
                    ]),
                    direction="down",
                    showactive=True,
                    x=0.8,
                    xanchor="center",
                    y=1.2,
                    yanchor="top"
                ),
            ]
        )
        fig.update_yaxes(range=[0, 40])  # 設定 y 軸的範圍，例如 0 到 50

    # update_layout(line_chart,"折線")
    update_layout(bar_chart,"長條")
    
    # line_chart.show()
    bar_chart.show()
    # # 生成HTML文件
    # line_chart.write_html('line_chart.html')
    bar_chart.write_html(f'bar_agehouseprice_{dis}.html')



def year_30avg_houseprice(data1,year,dis):
    """
    單一年度單一區域的每月平均房價趨勢，x軸為'月份'，y軸為'square_price(萬/坪)'，color='區域'，圖表區塊(facet_col)為type。
    參數放入dataframe資料，
    生成圖表的html以及顯示圖表。
    """
    #複製dataframe來進行操作
    df = data1.copy()
    # 將日期欄位轉換成欄位
    df['年份'] = pd.to_datetime(df['date']).dt.year
    df["月份"] = pd.to_datetime(df['date']).dt.month

    average_prices = df.loc[(df["年份"]==int(year)) & (df["區域"]==f"{dis}")].groupby(["年份",'月份','type'])['square_price(萬/坪)'].mean().reset_index()

    # 繪製折線圖
    line_chart = px.line(average_prices, x='月份', y='square_price(萬/坪)',  color='type', line_group='type',title=f'{year}年{dis}每月單坪房價趨勢圖')
    line_chart.update_layout(
    yaxis_title="房價(萬/坪)",
    xaxis_title=f"{year}"
)
    
    # 加入篩選器元件
    def update_layout(fig,x):
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            label="全部",
                            method="update",
                            args=[{"visible": [True, True, True]},
                                {"title": f"{year}年{dis}每月單坪房價趨勢圖 - 全部"}]
                        ),
                        dict(
                            label="華廈",
                            method="update",
                            args=[{"visible": [False, False, True]},
                                {"title": f"{year}年{dis}每月單坪房價趨勢圖 - 華廈"}]
                        ),
                        dict(
                            label="公寓",
                            method="update",
                            args=[{"visible": [False, True, False]},
                                {"title": f"{year}年{dis}每月單坪房價趨勢圖 - 公寓"}]
                        ),
                        dict(
                            label="住宅大樓",
                            method="update",
                            args=[{"visible": [True, False, False]},
                                {"title": f"{year}年{dis}每月單坪房價趨勢圖 - 住宅大樓"}]
                        ),
                    ]),
                    direction="down",
                    showactive=True,
                    x=0.8,
                    xanchor="center",
                    y=1.2,
                    yanchor="top"
                ),
            ]
        )

        fig.update_yaxes(range=[15, 45])  # 設定 y 軸的範圍，例如 0 到 50
        fig.update_xaxes(range=[1, 12])  # 設定 x 軸的範圍，例如 0 到 50

    update_layout(line_chart,"折線")

    line_chart.show()
    # 生成HTML文件
    line_chart.write_html(f'line_year30price_{dis}_{year}.html')



def age_type_trading(data1,dis):
    #複製dataframe來進行操作
    df = data1.copy()
    # 將日期欄位轉換成年份欄位
    df['年份'] = pd.to_datetime(df['date']).dt.year

    #創屋齡group欄位
    # 將 age 在小於等於 10 的設為 "0-10"
    df["屋齡"] = np.where(df["age"] <= 10, "0-10年", "")
    # 將 age 在大於 10 且小於 20 的設為 "10-20"
    df.loc[(df["age"] > 10) & (df["age"] <= 20), "屋齡"] = "10-20年"
    df.loc[(df["age"] > 20) & (df["age"] <= 30), "屋齡"] = "20-30年"
    df.loc[(df["age"] > 30) , "屋齡"] = "30年以上"

    df['成交量'] = df.groupby(['年份',"區域", 'type','屋齡'])['年份'].transform('count')
    print(df.loc[df["屋齡"]=="10-20年"].head(100))

    #計算每年的平均房價，並設為索引
    total_trading = df.loc[df["區域"] == dis].groupby(['年份', 'type', '屋齡'])["成交量"].mean().reset_index() 

    # 繪製長條圖
    scatter_chart = px.scatter(total_trading,x='年份', y="成交量", color='type', facet_col="屋齡", \
                    title=f'{dis}各屋齡房型成交量')
    
    # 加入篩選器元件
    def update_layout(fig,x):
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            label="全部",
                            method="update",
                            args=[{"visible": [True, True, True,True, True, True,True]},
                                {"title": f"{dis}各屋齡房價成交量 - 全部"}]
                        ),
                        dict(
                            label="華廈",
                            method="update",
                            args=[{"visible":  [False, False, False,False,False, False, False,False,True,True,True,True]},
                                {"title": f"{dis}各屋齡房價成交量 - 華廈"}]
                        ),
                        dict(
                            label="公寓",
                            method="update",
                            args=[{"visible": [False, False, False,False,True, True, True,True,False,False]},
                                {"title": f"{dis}各屋齡房價成交量 - 公寓"}]
                        ),
                        dict(
                            label="住宅大樓",
                            method="update",
                            args=[{"visible": [True, True, True,True,False, False, False,False,False,False,False,False]},
                                {"title": f"{dis}各屋齡房價成交量 - 住宅大樓"}]
                        ),
                    ]),
                    direction="down",
                    showactive=True,
                    x=0.8,
                    xanchor="center",
                    y=1.2,
                    yanchor="top"
                ),
            ]
        )
        # fig.update_yaxes(range=[10, 700])  # 設定 y 軸的範圍，例如 0 到 50

    # update_layout(line_chart,"折線")
    update_layout(scatter_chart,"長條")
    
    # line_chart.show()
    scatter_chart.show()
    # # 生成HTML文件
    # line_chart.write_html('line_chart.html')
    scatter_chart.write_html(f'scatter_trading_{dis}.html')

def rate_consumerprice_rentprice(table):
    #複製dataframe來進行操作
    df = pd.read_sql(table,engine)
    df =  df.sort_values('date')
    # if table == "五大行庫平均房貸利率": yaxis = 'rate'
    # elif table == "消費者物價指數" or table == "租金指數": yaxis = 'country'
    # else : return 
    # 繪製折線圖
    line_chart = px.line(df, x='date', y=df.columns[1:],title=table)
    line_chart.update_layout(yaxis_title=f"全國{table}")

    line_chart.show()
    # 生成HTML文件
    line_chart.write_html(f'{table}.html')

if __name__ == '__main__':
    #每年綜合的平均房價
    totalyear_avg_houseprice(df)
    dis = ["文山區","新店區"]
    year = ["2015","2016","2017","2018","2019","2020"]
    otherdata = ["五大行庫平均房貸利率","住宅價格指數","可能成交指數","房價所得比","消費者物價指數","租金指數","貸款負擔率"]
    for i in otherdata:
        rate_consumerprice_rentprice(i)
    #每年每區的平均房價
    for index in dis:
        #每年不同屋齡房型的房價
        age_avg_houseprice(df,index)
        age_type_trading(df,index)
        for value in year:
            year_avg_houseprice(df,value,index)
            year_30avg_houseprice(df,value,index)



