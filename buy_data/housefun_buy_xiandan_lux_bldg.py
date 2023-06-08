import requests
from bs4 import BeautifulSoup
base_url = "https://buy.housefun.com.tw/region/%E6%96%B0%E5%8C%97%E5%B8%82-%E6%96%B0%E5%BA%97%E5%8D%80_c/7-_fr/%E9%9B%BB%E6%A2%AF%E5%A4%A7%E6%A8%93_type/?pg="
page_number = 1

result_list = []

def is_last_page(soup):
    # Find the anchor tag with the class "has-arrow"
    next_button = soup.find('li', class_='has-arrow')

    # If the anchor tag is not found, it means this is the last page
    return next_button is None

while True:
    # Make a GET request to the current page URL
    url = base_url + str(page_number)
    response = requests.get(url)
    html = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract and process the desired information
    districts = "Xindian"
    types = "lux_building"
    ping_numbers = [em.find(class_="number").text.strip() for em in soup.find_all(class_="ping-number")]
    discount_prices = [em.find(class_="number").text.strip() for em in soup.find_all(class_="discount-price")]
    
    # Calculate the unit prices by dividing discount price by square
    # unit_prices = [f'{float(discount_price.replace(",", "")) / float(ping_number):.2f}' for discount_price, ping_number in zip(discount_prices, ping_numbers)]
    
    for ping_number, discount_price  in zip(ping_numbers, discount_prices):
        # Create a dictionary to store the extracted information for each item
        if ping_number == '--':
            continue
        else:
            unit_price = float(discount_price.replace(",", "")) / float(ping_number)
            data = {
                "district": districts,
                "type": types,
                "square": ping_number,
                "square_price":  f"{unit_price:.2f}",
                "total_price": discount_price
            }
        
        # Append the dictionary to the result list
        result_list.append(data)

    # Check if the last page has been reached
    if is_last_page(soup):
        break

    # Increment the page number for the next iteration
    page_number += 1

# Print the extracted information for each item
for item in result_list:
    print(item)

# You can access the result_list outside the loop for further processing
print("Total items:", len(result_list))

import json

# Your code for extracting data and populating result_list

# Define the output JSON file path
output_file = 'output_housefun_buy_xiandan_lux_bldg.json'

# Write the result_list to the JSON file with proper encoding
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result_list, f, ensure_ascii=False)

print("Data exported to", output_file)

