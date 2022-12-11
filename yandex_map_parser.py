import os
import sub
import sys
import zipfile
import warnings
from time import sleep
from loguru import logger
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

warnings.filterwarnings('ignore')

URL = "https://yandex.ru/maps"

useragent = ("user-agent=Mozilla/5.0 (X11; Linux x86_64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/106.0.0.0 Safari/537.36")

PATH_TO_DRIVER = ('/home/roman/real_python/webdriver/chromedriver')

logger.remove(0)
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> {level} "
           "<blue>{message}</blue>", level="DEBUG")
logger.add('data/Журнал_обработанных_данных.log',
           format=" {time:HH:mm:ss} {level} {line} {message}",
           level="DEBUG")


def create_data_folder():
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("data/parts"):
        os.mkdir("data/parts")


def get_driver_chrome():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = 'eager'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True
    driver = webdriver.Chrome(executable_path=PATH_TO_DRIVER,
                              options=options, desired_capabilities=caps)
    stealth(driver, user_agent=useragent, languages=["en-US", 'en'],
            vendor="Google Inc.", platform="Win32",
            webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    return driver


def ask_user_questions():
    try:
        answer = input(sub.questions)
        print()
        if answer.lower() == '2':
            city, start_value = sub.city_list, 0
            sub.create_file_for_links()
            sub.сreate_excel_tables()
            request, num_handled = input(sub.question_3), 0
        elif answer == '3':
            num_saved = int(input(sub.question_4))
            city = sub.city_list[num_saved:]
            start_value = input(sub.question_2)
            request, num_handled = input(sub.question_3), 0
        elif answer == '4':
            num_handled = input(sub.question_5)
            city, start_value, request = {}, 0, None
            logger.info('Обработка началась...')
        elif answer == '1':
            name_city = input('Введите название города\n').lower()
            city, start_value, num_handled = [(1, name_city)], 0, 0
            request = input(sub.question_3).lower()
            sub.сreate_excel_tables()
            sub.create_file_for_links()
        elif answer == '5':
            city, start_value, request, num_handled = {}, 0, None, 0
            sub.сreate_excel_tables()
            logger.info('Обработка началась...')
        return city, request, int(start_value), int(num_handled)
    except Exception:
        input('ОПЕЧАТКА!!! Перезапустите программу и введите данные еще раз')


def input_city_and_request(driver, curent_city, request):
    try:
        driver.get(URL)
        sleep(1)
        driver.find_element(By.TAG_NAME, "input").send_keys(curent_city)
        driver.find_element(By.TAG_NAME, "input").send_keys(" " + request)
        driver.find_element(By.TAG_NAME, "button").click()
        sleep(1.5)
    except Exception:
        logger.error('Input data and request')


def create_backup_excel(partner_id):

    files = ["data/partners.xlsx", "data/reviews.xlsx", "data/services.xlsx"]
    if partner_id % 1000 == 0:
        archive = f"data/parts/part_[{str(partner_id)[:-3]}].zip"
        zip_func(archive, files)
        sub.сreate_excel_tables()
    elif partner_id % 2 == 0:
        archive = "data/backup_copy_excel 1.zip"
        zip_func(archive, files)
    else:
        archive = "data/backup_copy_excel 2.zip"
        zip_func(archive, files)


def zip_func(archive, files):

    with zipfile.ZipFile(archive, "w") as zf:
        for file in files:
            zf.write(file)


def scroll_page_down_links(driver, actions):
    '''Srcoll down for all  links seeing'''
    try:
        clickable_element = (driver.find_element(By.CLASS_NAME,
                             "search-list-view__content")
                             .find_element(By.TAG_NAME, "div"))
        actions.click(clickable_element).perform()
        moving_down(driver)
    except Exception:
        logger.error('Scroll links')


def moving_down(driver):
    try:
        num_of_pushing_page_down = 22
        page_scrolling = driver.find_element(By.TAG_NAME, "body")
        while True:  # srcoll action
            num_links_before_scroll = len(driver.find_elements(By.CLASS_NAME,
                                          "search-snippet-view"))
            for i in range(num_of_pushing_page_down):
                page_scrolling.send_keys(Keys.PAGE_DOWN)
                sleep(0.4)
            num_links_after_scroll = len(driver.find_elements(By.CLASS_NAME,
                                         "search-snippet-view"))
            if num_links_after_scroll > num_links_before_scroll:  # comparison
                continue
            else:
                break
    except Exception:
        logger.error('Moving down links')


def save_all_links(source, num_links):
    try:
        temp_list_for_links = []
        soup = BeautifulSoup(source, "lxml")
        all_links = (soup.find("ul", class_="search-list-view__list")
                         .find_all("a", class_="search-snippet-view__"
                                   "link-overlay _focusable"))
        for i in all_links:
            text = i.get("href")
            curent_link = f"{(num := num_links())} https://yandex.ru{text}"
            temp_list_for_links.append(curent_link)
        sub.save_links_in_txt(temp_list_for_links)
        return num, len(temp_list_for_links)
    except Exception:
        logger.error('Save links')


def get_all_links(current_city, request, num_links, driver):
    try:
        logger.info(f'Идет сбор ссылок в городе {current_city[0]}'
                    f' {current_city[1]}')
        actions = ActionChains(driver)
        input_city_and_request(driver, current_city[1], request)
        scroll_page_down_links(driver, actions)
        num, sum_links = save_all_links(driver.page_source, num_links)
        logger.info(f'Для города {current_city[0]} {current_city[1]} '
                    f'собрано {sum_links} шт., собрано всего {num} шт.')
    except Exception:
        driver.close()
        driver.quit()
        logger.info("ОШИБКА ДАННЫХ ИЛИ СЕТИ")


def delete_dublicate_links():
    with open("data/links.txt") as file:
        temp_list = file.readlines()
        old_list = [i.split()[1] for i in temp_list]
    new_list = []
    [new_list.append(item) for item in old_list if item not in new_list]

    with open("data/links.txt", 'w') as file:
        a = 1
        for link in new_list:
            file.write(f'{a} {link}\n')
            a += 1


def get_data_for_partner_table(link, partner_id, driver) -> int:
    try:
        driver.get(link)
        sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        empty_line = ''
        result_list = [
            partner_id, 'компания',
            sub.get_name_of_partner(soup), empty_line,
            sub.get_phone_number(soup), empty_line,
            sub.get_address(soup), empty_line,
            empty_line, sub.get_messenger(soup, 'telegram'),
            sub.get_messenger(soup, 'whatsapp'), empty_line,
            sub.get_messenger(soup, 'vkontakte'), sub.get_website(soup),
            empty_line, sub.get_logo_link(soup),
            sub.get_coordinates(driver)[1], sub.get_coordinates(driver)[0],
            sub.get_photos_links(driver, link)]
        return result_list
    except Exception:
        driver.close()
        driver.quit()
        logger.error("ОШИБКА ДАННЫХ ИЛИ СЕТИ")


def get_data_for_reviews_table(link, partner_id, driver):
    try:
        driver.get(f'{link}reviews')
        sleep(1)
        sub.scroll_page_down_reviews(driver)
        soup = BeautifulSoup(driver.page_source, "lxml")
        all_reviews = sub.get_all_reviews(soup)
        reviews_list = []
        if all_reviews:
            for one_block in all_reviews:
                current_review = get_current_review_row(one_block, partner_id)
                reviews_list.append(current_review)
        return reviews_list
    except Exception:
        driver.close()
        driver.quit()
        logger.error("ОШИБКА ДАННЫХ ИЛИ СЕТИ")


def get_current_review_row(one_block, partner_id):
    empty_line = ''
    return [
        partner_id,
        sub.get_name_client(one_block),
        sub.get_rating(one_block),
        sub.get_date_review(one_block),
        sub.get_text_review(one_block),
        empty_line
        ]


def get_data_for_services_table(link, partner_id, driver):
    try:
        driver.get(f'{link}prices')
        sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        all_services = sub.get_all_serevices(soup)
        if all_services:
            services_list = []
            for one_sevice in all_services:
                current_service = [partner_id,
                                   sub.get_name_service(one_sevice),
                                   sub.get_price(one_sevice)]
                services_list.append(current_service)
            return services_list
    except Exception:
        driver.close()
        driver.quit()
        logger.error("ОШИБКА ДАННЫХ ИЛИ СЕТИ")


def process_all_links(num_handled, driver):

    delete_dublicate_links()
    with open("data/links.txt", "r") as file:
        for row in file:
            link = row.strip().split()[1]
            partner_id = int(row.strip().split()[0])
            if num_handled >= partner_id:
                continue
            get_all_data(partner_id, link, driver)
    logger.info(f'Обработка ссылок окончена! Всего {partner_id} ссылок')


def get_all_data(partner_id, link, driver):

    try:
        partners_list = get_data_for_partner_table(link, partner_id, driver)
        reviews_list = get_data_for_reviews_table(link, partner_id, driver)
        services_list = get_data_for_services_table(link, partner_id, driver)
        sub.append_data_table_partners(partners_list)
        sub.append_data_table_reviews(reviews_list)
        sub.append_data_table_services(services_list)
        logger.info(f'Идет обработка ссылок, {partner_id} сохранена')
        if partner_id % 25 == 0:
            create_backup_excel(partner_id)
    except Exception:
        driver.close()
        driver.quit()
        logger.error("ОШИБКА ДАННЫХ ИЛИ СЕТИ")


def main():
    try:
        driver = get_driver_chrome()
        create_data_folder()
        city, request, start_value, num_handled = ask_user_questions()
        num_links = sub.counter(start_value)
        for current_city in city:
            sub.create_file_for_links()
            get_all_links(current_city, request, num_links, driver)
        process_all_links(num_handled, driver)
    except Exception:
        logger.info('ПЕРЕЗАПУСТИТЕ ПРОГРАММУ')
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
