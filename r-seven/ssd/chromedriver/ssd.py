from bs4 import BeautifulSoup
import json
import requests
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

xpath = '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div/a[5]'
url = 'https://r-seven.ru/catalog/ssd/?PAGEN_1=1'

headers = {
    'accept': 'accept',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

disk_all = []
replace = ['\n', '\t', '\"']
links = ['https://r-seven.ru/catalog/ssd/?PAGEN_1=1']

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(
    executable_path='C:\\Users\\Petr\\Desktop\\Python projects\\r-seven\\ssd\\chromedriver\\chromedriver.exe',
    options=options)


def take_info():
    for end in links:
        print(end)
        req = requests.get(end, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        all_disk = soup.find_all(class_='page__list-content-item')

        for disk in all_disk:
            price = disk.find(class_='card-list__price').text

            #   name = disk.find(class_='card-list').find(class_='card-list__inner').find(class_='card-list__wrapper').find(class_='card-list__wrapper-info').find('a').text
            name = disk.find(class_='card-list__wrapper-info').find('a').text

            description = disk.find(class_='card-list__list').text

            for item in replace:
                if item in description:
                    description = description.replace(item, '')

            disk_all.append(
                {
                    'name': name,
                    'price': price,
                    'description': description
                }
            )

            print(f'{name} - {price}')

    with open('disk.json', 'w', encoding='utf-8') as file:
        json.dump(disk_all, file, indent=4, ensure_ascii=False)


def next_page():
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')

    urls = soup.find_all(class_='pagination__item')

    for i in urls:
        link = i.get('href')
        if link == '#':
            pass
        else:
            link = 'https://r-seven.ru' + link
            links.append(link)


try:
    driver.get(url=url)
    time.sleep(1)

    while True:

        button = driver.find_element(By.XPATH, xpath)
        button.click()

        url = links[-1]

        next_page()

        time.sleep(1)

        for elem in links:
            if elem == 'https://r-seven.ru/catalog/ssd/?&PAGEN_1=1':
                links.remove(elem)
            links = list(set(links))
            links.sort()
            if elem[-1] == str(9):
                pass
            links.sort(key=len)

        with open('link_ssd.json', 'w') as file:
            json.dump(links, file, indent=4, ensure_ascii=False)


except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()


def main():
    take_info()


if __name__ == '__main__':
    main()


