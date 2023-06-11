import pymysql,os
from sqlalchemy import create_engine
import pandas as pd

#
engine = create_engine("mysql+pymysql://mysql帳號:mysql密碼@localhost/資料庫名稱?charset=utf8")

data_file=os.listdir("D:\\practice\\house_price_comparison\\opendata\\refresh_data")
print(data_file)
for file in data_file:
      if ".csv" not in file: 
        continue
      df = pd.read_csv(file)
      print(df.head(10))
      #"opendata_Wenshan"及"opendata_Xindia"為資料表名稱
      if "Wenshan" in file:
          df.to_sql("opendata_Wenshan",engine,index=False,if_exists="append")
      else:
          df.to_sql("opendata_Xindia",engine,index=False,if_exists="append")
      

