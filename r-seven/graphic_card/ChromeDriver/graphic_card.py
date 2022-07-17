import json
import requests
from bs4 import BeautifulSoup
import csv
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

xpath = '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div/a[5]'
url = 'https://r-seven.ru/catalog/video/?PAGEN_1=1'

headers = {
    'accept': 'accept',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

cards_name = []
cards_price = []
cards_name_price = []
urs = ['https://r-seven.ru/catalog/video/?PAGEN_1=1']

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path='C:\\Users\\Petr\Desktop\\Python projects\\r-seven\\graphic_card\\ChromeDriver\\chromedriver.exe',
                          options=options)


def take_info():
    for item in urs:
        print(item)
        req = requests.get(item, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        all_cards = soup.find_all(class_='page__list-content-item')

        for card in all_cards:
            card_name = card.find(class_='card-list__wrapper-info').find('a').text
            cards_name.append(card_name)

            card_price = card.find(class_='card-list__price').text
            cards_price.append(card_price)

            cards_name_price.append(
                {
                    'card name': card_name,
                    'card price': card_price
                }
            )

            with open('graphic_card_end.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';', lineterminator='\n')
                writer.writerow(
                    (
                        card_name,
                        card_price
                    )
                )

            print(f'{card_name} - {card_price}')

    with open('graphic_card_end.json', 'w', encoding='utf-8') as file:
        json.dump(cards_name_price, file, indent=4, ensure_ascii=False)


def next_page():
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    urls = soup.find_all(class_='pagination__item')

    for i in urls:
        urle = i.get('href')
        if urle == '#':
            pass
        else:
            urle = 'https://r-seven.ru' + urle
            urs.append(urle)

    with open('urls.json', 'w') as file:
        json.dump(urs, file, indent=4, ensure_ascii=False)


try:
    driver.get(url=url)
    time.sleep(1)

    while True:

        button = driver.find_element(By.XPATH, xpath)
        button.click()

        url = urs[-1]

        next_page()

        time.sleep(5)

        for elem in urs:
            if elem == 'https://r-seven.ru/catalog/video/?&PAGEN_1=1':
                urs.remove(elem)
            urs = list(set(urs))
            urs.sort()
            if elem[-1] == str(9):
                pass
            urs.sort(key=len)

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()


def main():
    take_info()


if __name__ == '__main__':
    main()
