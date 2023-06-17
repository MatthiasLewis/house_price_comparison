import os
from sqlalchemy import create_engine
import pandas as pd
import sqlite3

#sqlite為python內建資料庫格式，data.db為資料庫格式。
engine = create_engine("sqlite:///data.db?charset=utf8")
#engine = create_engine("mysql+pymysql://username:password@localhost/databsename?charset=utf8")

data_file=os.listdir("D:\\practice\\house_price_comparison\\opendata\\refresh_data")
print(data_file)
for file in data_file:
    if ".csv" not in file: 
        continue
    df = pd.read_csv(file)
    print(file.partition(")")[0])
    #"opendata_Wenshan"及"opendata_Xindia"為資料表名稱
    if "Wenshan" in file:
        df.to_sql("opendata_Wenshan",engine,index=False,if_exists="append")
    elif "Xindia" in file:
        df.to_sql("opendata_Xindia",engine,index=False,if_exists="append")
    else:
        file = file.partition(")")[0]
        df.to_sql(file[7:],engine,index=False,if_exists="replace")
      

# # 连接到SQLite数据库
# conn = sqlite3.connect('data.db')
# # 创建游标对象
# cursor = conn.cursor()
# # 执行SQL语句
# cursor.execute('SELECT rate FROM 五大行庫平均房貸利率')
# # 获取查询结果
# result = cursor.fetchall()
# for row in result[:10]:
#     print(row)
# # 关闭游标和数据库连接
# cursor.close()
# conn.close()
      

