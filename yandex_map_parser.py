# import re
import os
# import random
import warnings
from time import sleep

import sub
from bs4 import BeautifulSoup
from loguru import logger
# from cities import all_cities
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth

warnings.filterwarnings('ignore')

URL = "https://yandex.ru/maps"

DATA_FOLDER = '/home/roman/real_python/web_parsing/yandex_map_parser'

PATH_TO_CHROME_DRIVER = f'{DATA_FOLDER}/chromedriver'

useragent = ("user-agent=Mozilla/5.0 (X11; Linux x86_64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/106.0.0.0 Safari/537.36")

counter_of_partners = sub.counter()

logger.add(f'{DATA_FOLDER}/data/log.log',
           format="[{time:HH:mm:ss}] {level} {message} ",
           level="DEBUG",
           rotation='30 MB', compression='zip', retention=None)


def create_data_folder():
    if not os.path.exists(f"{DATA_FOLDER}/data"):
        os.mkdir(f"{DATA_FOLDER}/data")


def get_driver_chrome():

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.headless = False
    driver = webdriver.Chrome(
            executable_path="Parser-of-Yandex-Maps-main/chromedriver",
            options=options)
    stealth(driver, user_agent=useragent, languages=["en-US", 'en'],
            vendor="Google Inc.", platform="Linux",
            webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    return driver


def ask_user_city_and_request():

    city = input("Введите:\nа) <Название города> - для анализа "
                 "по одному городу,\n"
                 "б) Слово <Все>' - для анализа всех городов России "
                 "с населением более 100 тысяч человек...\n")

    request = input("Введите сферу, которую хотите обработать..\n")

    return city, request


def input_city_and_request(driver, city, request):
    try:
        driver.get(URL)
        sleep(2)
        driver.find_element(By.TAG_NAME, "input").send_keys(city)
        driver.find_element(By.TAG_NAME, "input").send_keys(" " + request)
        driver.find_element(By.TAG_NAME, "button").click()
        sleep(1.5)
    except Exception as ex:
        logger.error('ошибка при вводе поисковый данных', ex)
        sleep(10)
        input_city_and_request(driver, city, request)


@logger.catch
def scroll_page_down_links(driver, actions):
    '''Srcoll down for all main links seeing'''
    try:
        num_of_pushing_page_down = 18
        clickable_element = (driver.find_element(By.CLASS_NAME,
                             "search-list-view__content")
                             .find_element(By.TAG_NAME, "div"))
        actions.click(clickable_element).perform()
        page_scrolling = driver.find_element(By.TAG_NAME, "body")
        while True:  # srcoll action
            num_links_before_scroll = len(driver.find_elements(By.CLASS_NAME,
                                          "search-snippet-view"))
            for i in range(num_of_pushing_page_down):
                page_scrolling.send_keys(Keys.PAGE_DOWN)
                sleep(0.1)
            num_links_after_scroll = len(driver.find_elements(By.CLASS_NAME,
                                         "search-snippet-view"))
            if num_links_after_scroll > num_links_before_scroll:  # comparison
                continue
            else:
                break
    except Exception as ex:
        logger.error("Ошибка при скролинге страницы", ex)


def scroll_page_down_reviews(driver, actions):
    '''Scrolling down for all reviews seeing'''
    try:
        num_of_pushing_page_down = 18
        clickable_element = (driver.find_element(By.TAG_NAME,
                             "h1"))
        actions.click(clickable_element).perform()
        page_scrolling = driver.find_element(By.TAG_NAME, "body")
        while True:  # srcoll action
            num_links_before_scroll = len(driver.find_elements(By.CLASS_NAME,
                                          "business-review-view__info"))
            for i in range(num_of_pushing_page_down):
                page_scrolling.send_keys(Keys.PAGE_DOWN)
                sleep(0.1)
            num_links_after_scroll = len(driver.find_elements(By.CLASS_NAME,
                                         "business-review-view__info"))
            if num_links_after_scroll > num_links_before_scroll:  # comparison
                continue
            else:
                break
    except Exception as ex:
        logger.error(ex)


@logger.catch
def save_all_links(source):
    try:
        temp_list_for_links = []
        soup = BeautifulSoup(source, "lxml")
        all_links = (soup.find("ul", class_="search-list-view__list")
                         .find_all("a", class_="search-snippet-view__"
                                   "link-overlay _focusable"))
        for i in all_links:
            text = i.get("href")
            curent_link = f"https://yandex.ru{text}"
            temp_list_for_links.append(curent_link)

        save_links_in_txt(temp_list_for_links)
    except Exception as ex:
        logger.error('Ошибка при сохранении ссылок в файл', ex)


def create_file_for_links():
    with open("links.txt", 'w') as file:
        file.write('')


def save_links_in_txt(list):
    with open(f"{DATA_FOLDER}/data/links.txt", 'a') as file:
        for link in list:
            file.write(f'{link}\n')


@logger.catch
def get_all_links():

    try:
        driver = get_driver_chrome()
        actions = ActionChains(driver)
        input_city_and_request(driver, city, request)
        scroll_page_down_links(driver, actions)
        save_all_links(driver.page_source)
        logger.info('Ссылки собраны')
    except Exception as ex:
        logger.error(ex)
    finally:
        driver.close()
        driver.quit()


def get_data_for_partner_table(driver, link, city, partner_id) -> int:
    driver.get(link)
    sleep(1)
    soup = BeautifulSoup(driver.page_source, "lxml")
    result_list = [
        partner_id,
        city,
        sub.get_name_of_partner(soup),
        sub.get_phone_number(soup),
        sub.get_address(soup),
        sub.get_website(soup),
        sub.get_messenger(soup, 'whatsapp'),
        sub.get_messenger(soup, 'telegram'),
        sub.get_messenger(soup, 'vkontakte'),
        sub.get_messenger(soup, 'viber'),
        sub.get_logo_link(soup),
        sub.get_coordinates(driver)[1],
        sub.get_coordinates(driver)[0],
        sub.ger_photos_links(driver, link)
    ]
    sub.append_data_table_partners(result_list)
    return partner_id


def get_data_for_reviews_table(driver, link, partner_id):
    try:
        driver.get(f'{link}reviews')
        actions = ActionChains(driver)
        sleep(0.5)
        scroll_page_down_reviews(driver, actions)
        soup = BeautifulSoup(driver.page_source, "lxml")
        all_reviews = sub.get_all_reviews(soup)
        for one_block in all_reviews:
            current_review = [
                partner_id,
                sub.get_name_client(one_block),
                sub.get_rating(one_block),
                sub.get_date_review(one_block),
                sub.get_text_review(one_block)
            ]
            sub.append_data_table_reviews(current_review)
    except Exception as ex:
        logger.warning(ex)


def get_data_for_services_table(driver, link, partner_id):
    driver.get(f'{link}prices')
    sleep(1)
    soup = BeautifulSoup(driver.page_source, "lxml")
    all_services = sub.get_all_serevices(soup)
    for one_sevice in all_services:
        current_service = [
            partner_id,
            sub.get_name_service(one_sevice),
            sub.get_price(one_sevice)
        ]
        sub.append_data_table_services(current_service)


def process_all_links(city):
    driver = get_driver_chrome()
    with open(f"{DATA_FOLDER}/data/links.txt", "r") as file:
        try:
            for link in file:
                partner_id = counter_of_partners()
                get_data_for_partner_table(driver, link, city, partner_id)
                get_data_for_reviews_table(driver, link, partner_id)
                get_data_for_services_table(driver, link, partner_id)
        except Exception as ex:
            logger.error(ex)
        finally:
            driver.close()
            driver.quit()


if __name__ == '__main__':

    city, request = 'Миасс', 'стоматология'   # ask_user_city_and_request()
    create_data_folder()
    # get_all_links(city, request)
    # create_file_for_links()
    sub.сreate_excel_tables()
    process_all_links(city)
