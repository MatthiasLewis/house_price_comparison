from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'notifications': 2}}  # gives permission to pop-up window
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(options=options)

# get website
url = 'https://rent.housefun.com.tw/region/%E5%8F%B0%E5%8C%97%E5%B8%82_%E6%96%87%E5%B1%B1%E5%8D%80/?cid=0000&aid=12&purpid=4,3,2,1'

driver.get(url)

district = 'Wenshan'

# empty data list to append items later
data_list = []

# start from page 1
page = 1
while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')    # page_source get HTML
    articles = soup.findAll('article',class_="DataList both")
    for article in articles:
        # Extract the required information
        district = "Wenshan"
        # title = article.select_one('h3.title a').text.strip()
        # address = article.select_one('address.addr').text.strip()
        total_price = article.select_one('.info li.InfoList:nth-of-type(1) span.infos').text.strip().replace(' 元/月', '')
        square = article.select_one('.info li.InfoList:nth-of-type(2) span.infos').text.strip().replace(' 坪', '')
        # landlord = article.select_one('.info li.InfoList:nth-of-type(3) span.infos').text.strip()
        # last_updated = article.select_one('.info li.InfoList:nth-of-type(4) span.infos').text.strip()
        # room_info = article.select_one('.sectionList .level').text.strip()
        floor_info = article.select_one('.sectionList .pattern').text.strip()

        # Clean and convert total_price
        total_price = ''.join(filter(str.isdigit, total_price))
        total_price = int(total_price)

        # Clean and convert square
        square = ''.join(filter(str.isdigit, square))
        square = int(square) if square else 0  # Assign 0 if square is empty

        # Calculate price per square
        square_price = round(total_price / square, 2) if square != 0 else 0        


        # assign building type
        try:
            floor_number, total_floors = floor_info.split('：')[1].split('/')
            if int(total_floors)<= 6:
                building_type = 'building'
            else:
                building_type = 'lux_building' 
        except:
            floor_number = 'null'   # 有些沒資訊，會寫 "樓層：--"
            total_floors = 'null'
            building_type = 'null'
            

        # Store the extracted information in dict
        data_dict = {
            'district': district,
            # 'title': title,
            # 'address': address,
            'total_price': total_price,
            'square': square,
            'square_price': square_price,
            # 'landlord': landlord,
            # 'last_updated': last_updated,
            # 'room_info': room_info,
            'floor_number': floor_number.strip(),
            'total_floors': total_floors.strip(),
            'building_type': building_type
        }
        # print(title)

        # append all the dict to the list
        data_list.append(data_dict)

    
    print(page)
    print(len(data_list))
    
    # print page number
    page+=1
    
    # do this if error then break
    try:

        # keeps clicking until there is no more next arrow
        next_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//li[@class="has-arrow"]/a[@onclick="PM({page})"]')))
        driver.execute_script("arguments[0].click();", next_button)
        
        # pause in seconds
        sleep(3)  
    except:
        break

# close brower
driver.quit()
print(data_list)

import json
with open("housefun_rent.json", "w", encoding='utf-8') as file:
    file.write(json.dumps(data_list, ensure_ascii=False))
