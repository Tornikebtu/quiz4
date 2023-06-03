import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randint
payloads = {'dispatch':'products.on_sale','page': 1}
url = 'https://ch.ge/index.php'
file = open('product.csv', 'w', newline='\n', encoding='UTF-8_sig')
csv_obj = csv.writer(file)
csv_obj.writerow(['დასახელება', 'ახალი ფასი', 'ფასდაკლება', 'დანაზოგი', 'ძველი ფასი'])


while requests.get(url, params=payloads) != '<Response [404]>':
    response = requests.get(url, params=payloads)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    small_soup = soup.find('div', class_ = 'span12')
    product_wrapper = small_soup.find('div', id = 'products_on_sale_pagination_contents')
    all_product = product_wrapper.find_all('div', class_ = 'ty-column4')

    for product in all_product:
        title = product.h4.a.text
        old_price = product.find('span', class_='ty-strike')
        updated_price = product.find('span', class_='ty-price-num')
        sale_percent = product.find('div', class_='ty-product-labels__item--discount')
        old_price = float(old_price.span.text)
        updated_price = float(updated_price.text)
        sale_percent = sale_percent.em.text
        savings = (old_price - updated_price)
        savings = f'{savings:.2f}'
        print(title, updated_price, sale_percent, savings, old_price)
        csv_obj.writerow([title, updated_price, sale_percent, savings, old_price])
    print(response.url)
    payloads['page'] += 1
    sleep(randint(5,10))