from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json,time
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

# search_url={"文山區":"%E5%8F%B0%E5%8C%97%E5%B8%82/116","新店區":"%E6%96%B0%E5%8C%97%E5%B8%82/231"}
#新店區url = "https://www.hbhousing.com.tw/BuyHouse/%E6%96%B0%E5%8C%97%E5%B8%82/231"
url = "https://www.hbhousing.com.tw/BuyHouse/%E5%8F%B0%E5%8C%97%E5%B8%82/116"
options = webdriver.ChromeOptions()
options.add_argument("incognito")
driver = webdriver.Chrome(options = options)
driver.get(url)
wait = WebDriverWait(driver, 10)

data =[]
while True :
    soup = BeautifulSoup(driver.page_source,"html.parser")   #取動態原始碼
    result = soup.find_all("div", {"class":"item__main"})
    for value in result:
        value2 = value.find("div",class_="item__info")
        if "土地" in value2.text:
            continue
        #屋齡age
        item_age = value2.find("div", class_="item__info__table").find_all("li")[-2]
        age=item_age.text.replace("\n","").strip()
        #建坪square
        item_square = value2.find("div",class_="item__info__header").find_all("span",class_="color--black")[-1]
        square = item_square.text.replace("\n","").strip()
        #住宅型態type
        item_type = value2.find("div", class_="item__info__table").find("ul").find_all("li")[-3]
        type_ = item_type.text.replace("\n","").strip()
        #總價total_price
        item_price = value2.find("div",class_="item__info__header").find("span",class_="hlight color--red")
        total_price = item_price.text.replace("\n","").strip()
        #單坪價格(總價/坪數)square_price
        item_square_price = float(total_price)/float(square)
        square_price = round(item_square_price,2)
        #其他search
        item_search = value2.find("div",class_="item-intro").find("ul",class_="item__features").find_all("li")
        search = []
        for i in item_search:
            search.append ( i.text.replace("\n","").strip())
        data.append({'district':"文山區",
                    "age":age,
                    "square":float(square),
                    "square_price":square_price,
                    "type":type_,
                    "total_price": int(total_price),
                    "search":search
                    })
        
    try:
        next_page= driver.find_element(By.XPATH, '//li/a[text()=">"]')
        next_page.click()
        time.sleep(randint(10,15))
    except: # 如果沒有下一頁就跳出迴圈
        print("結束爬取資料～")
        break

with open (f"buy_文山區.json","w",encoding="utf8") as f:
    json.dump(data,f,ensure_ascii=False)
