from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json,time
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

url = "https://www.hbhousing.com.tw/RentHouse/"
options = webdriver.ChromeOptions()
options.add_argument("incognito")
driver = webdriver.Chrome(options = options)
driver.get(url)
wait = WebDriverWait(driver, 10)

# 找到區域點擊下拉選單=>新北市=>點擊下拉選單=>新店區=>立即搜尋
element =driver.find_element(By.CSS_SELECTOR, 'div.selectform.selectpush.where')
element.click()
time.sleep(randint(3,5))
element2 =driver.find_element(By.XPATH,'//li[contains(label, "新北市")]')
element2.click()
time.sleep(randint(3,5))
element3 = driver.find_element(By.CSS_SELECTOR, "div.selectform.selectpush.where.active ul.selectpanel.selblock02 li input[value='231']")
element3.click()
time.sleep(randint(3,5))
search_button = driver.find_element(By.CLASS_NAME, "button--search")
search_button.click()
time.sleep(randint(3,5))

soup = BeautifulSoup(driver.page_source,"html.parser")
result = soup.find_all("div",class_="rent__list__item")
data =[]
while True:
    for value in result:
        if "收納" in value.text or "店面" in value.text or "店辦" in value.text or "賣場" in value.text or "其他" in value.text:
            continue
        value2 = value.find("div",class_="item__info").find("div",class_="item__info__header")
        square = value2.find_all("span",class_="color--black")[-1].text
        if square == "":
            continue
        print("建坪:",square)
        total_price = value2.find("span",class_="hlight color--red").text
        print("租金:",total_price)
        value3 = value.find("div",class_="item__info__table")
        age_text = value3.find_all("div",class_="item__info__td")[-1].text
        age = re.search(r'([\d.]+)', age_text).group(1)
        print("屋齡:",age)
        type_ = value3.find_all("div",class_="item__info__td")[-5].text
        print("房屋類型:",type_)
        square_price = float(total_price)/float(square)
        print("單坪:",square_price)
        item_search = value.find("div",class_="item__main").find("ul",class_="item__features").find_all("li")
        search = []
        for i in item_search:
            search.append ( i.text.replace("\n","").strip())
        print("其他:",search)
        data.append({'district':"新店區",
                            "age":age,
                            "square":float(square),
                            "square_price":square_price,
                            "type":type_,
                            "total_price": float(total_price),
                            "search":search
                            })
    try:
        next_page= driver.find_element(By.XPATH, '//a[contains(text(), ">")]')
        next_page.click()
        time.sleep(randint(10,15))
    except: # 如果沒有下一頁就跳出迴圈
        print("結束爬取資料～")
        break    
# print(data)
with open (f"rent_新店區.json","w",encoding="utf8") as f:
    json.dump(data,f,ensure_ascii=False)
