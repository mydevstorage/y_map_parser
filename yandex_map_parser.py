# import re
# import random
# import requests
# import argparse
from time import sleep
from loguru import logger
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

logger.add('log.log', format="[{time:HH:mm:ss}] {level} {message} ",
           level="DEBUG",
           rotation='30 MB', compression='zip', retention=None)


DATA = []
num_of_page = 1
URL = "https://yandex.ru/maps"

DATA_FOLDER = '/home/roman/real_python/web_parsing/yandex_map_parser'

PATH_TO_CHROME_DRIVER = f'{DATA_FOLDER}/chromedriver'

user_agent = ("user-agent=Mozilla/5.0 (X11; Linux x86_64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/106.0.0.0 Safari/537.36")


def get_driver_chrome():

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.headless = True
    driver = webdriver.Chrome(
            executable_path="Parser-of-Yandex-Maps-main/chromedriver",
            options=options)
    stealth(driver, user_agent=user_agent, languages=["en-US", 'en'],
            vendor="Google Inc.", platform="Linux",
            webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    return driver


def ask_user_city_and_request():

    city = input("Введите:\nа) <Название города> - для анализа "
                 "по одному городу,\n"
                 "б) Слово <Все>' - для анализа всех городов России "
                 "с населением более 100 тысяч человек...\n")

    request = input("Введите сферу, которую хотите обработать..\n ")

    return city, request


def input_city_and_request(driver, city, request):
    try:
        driver.get(URL)
        driver.find_element(By.TAG_NAME, "input").send_keys(city)
        driver.find_element(By.TAG_NAME, "input").send_keys(" " + request)
        driver.find_element(By.TAG_NAME, "button").click()
    except Exception:
        logger.error('Ошибка при вводе поисковых данных')
        input_city_and_request(driver, city, request)


def scroll_page_down(driver, actions):
    '''Srcoll down of all elements for a city'''
    try:
        num_of_pushig_page_down = 18
        clickable_element = (driver.find_element(By.CLASS_NAME,
                                "search-list-view__content")
                                .find_element(By.TAG_NAME, "div"))
        actions.click(clickable_element).perform()
        page_scrolling = driver.find_element(By.TAG_NAME, "body")
        search_name = driver.find_elements(By.CLASS_NAME, "search-snippet-view")
        while True:  # srcoll action
            num_befor_scroll = len(search_name)
            for i in range(num_of_pushig_page_down):
                page_scrolling.send_keys(Keys.PAGE_DOWN)
                sleep(0.1)
            if len(search_name) > num_befor_scroll:  # comparison
                continue
            else:
                break
    except Exception:
        logger.error("Ошибка при скролинге страницы")


def save_all_links(source):
    try:
        temp_list_for_links = []
        soup = BeautifulSoup(source, "lxml")
        all_links = (soup.find("ul", class_="search-list-view__list")
                         .find_all("a", class_="search-snippet-view__"
                                   "link-overlay _focusable"))
        for i in all_links:
            text = i.get("href")
            curent_link = f"https://yandex.ru/{text}"
            temp_list_for_links.append(curent_link)

        save_links_in_txt(temp_list_for_links)
    except Exception:
        logger.error('Ошибка при сохранении ссылок в файл')


def create_file_for_links():
    with open("yandex_map_parser/data/links.txt", 'w') as file:
        file.write('')


def save_links_in_txt(list):
    with open("yandex_map_parser/data/links.txt", 'a') as file:
        for link in list:
            file.write(f'{link}\n')


def get_all_links():
    driver = get_driver_chrome()
    actions = ActionChains(driver)
    create_file_for_links()
    try:
        city, request = ask_user_city_and_request()
        input_city_and_request(driver, city, request)
        scroll_page_down(driver, actions)
        save_all_links(driver.page_source)
    except Exception:
        logger.error('Общая ошибка при сборе ссылок')
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    get_all_links()
    logger.info('Ссылки собраны')
