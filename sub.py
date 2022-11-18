from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from loguru import logger

# DATA_FOLDER = '/home/roman/real_python/web_parsing/yandex_map_parser'
# DATA_FOLDER = 'yandex_map_parser'

all_cities = ['Калуга', 'Брянск', 'Майкоп', 'Санкт-Петербург', 'Новосибирск',
              'Казань', 'Нижний Новгород', 'Челябинск', 'Красноярск', 'Самара',
              'Уфа', 'Ростов-на-Дону', 'Омск', 'Краснодар', 'Воронеж', 'Пермь',
              'Волгоград', 'Саратов', 'Тюмень', 'Тольятти', 'Барнаул',
              'Ижевск', 'Махачкала', 'Хабаровск', 'Ульяновск', 'Иркутск',
              'Владивосток', 'Ярославль', 'Кемерово', 'Томск', 'Тула',
              'Набережные Челны', 'Севастополь', 'Владимир', 'Грозный',
              'Ставрополь', 'Оренбург', 'Новокузнецк', 'Рязань', 'Балашиха',
              'Пенза', 'Чебоксары', 'Липецк', 'Калининград', 'Астрахань',
              'Киров', 'Сочи', 'Курск', 'Улан-Удэ', 'Тверь', 'Рыбинск',
              'Магнитогорск', 'Сургут', 'Иваново', 'Якутск',
              'Симферополь', 'Белгород', 'Нижний Тагил', 'Чита',
              'Волжский', 'Смоленск', 'Подольск', 'Саранск', 'Вологда',
              'Череповец', 'Орёл', 'Архангельск', 'Владикавказ', 'Москва'
              'Йошкар-Ола', 'Стерлитамак', 'Мурманск', 'Кострома',
              'Тамбов', 'Химки', 'Мытищи', 'Нальчик', 'Таганрог', 'Нижнекамск',
              'Благовещенск', 'Комсомольск-на-Амуре', 'Петрозаводск',
              'Шахты', 'Энгельс', 'Великий Новгород', 'Люберцы',
              'Братск', 'Старый Оскол', 'Ангарск', 'Сыктывкар', 'Дзержинск',
              'Псков', 'Орск', 'Красногорск', 'Армавир', 'Абакан', 'Балаково',
              'Бийск', 'Южно-Сахалинск', 'Одинцово', 'Уссурийск',
              'Норильск', 'Волгодонск', 'Сызрань', 'Петропавловск-Камчатский',
              'Новочеркасск', 'Альметьевск', 'Златоуст', 'Северодвинск',
              'Хасавюрт', 'Керчь', 'Домодедово', 'Салават', 'Миасс',
              'Копейск', 'Пятигорск', 'Электросталь', 'Находка',
              'Березники', 'Коломна', 'Щёлково', 'Серпухов', 'Ковров',
              'Кисловодск', 'Батайск', 'Рубцовск', 'Обнинск', 'Кызыл',
              'Нефтеюганск', 'Назрань', 'Каспийск', 'Долгопрудный',
              'Новомосковск', 'Ессентуки', 'Невинномысск', 'Октябрьский',
              'Раменское', 'Первоуральск', 'Михайловск', 'Реутов', 'Черкесск',
              'Жуковский', 'Димитровград', 'Пушкино', 'Артём', 'Камышин',
              'Евпатория', 'Муром', 'Ханты-Мансийск', 'Новый Уренгой',
              'Арзамас', 'Ногинск', 'Новошахтинск', 'Бердск', 'Элиста',
              'Северск', 'Новочебоксарск', 'Дербент', 'Нефтекамск',
              'Орехово-Зуево', 'Каменск-Уральский', 'Новороссийск',
              'Нижневартовск', 'Курган', 'Королёв', 'Прокопьевск',
              'Екатеринбург',
              'Ачинск', 'Тобольск', 'Ноябрьск', 'Видное', 'Сергиев Посад']

city_list = [(number, city) for number, city in enumerate(all_cities, 1)]

questions = ("Введите:\n"
             "а) <Один город>, для обработки одного города,\n"
             "б) <Все>' - для анализа всех городов России "
             "с населением более 100 тысяч человек...\n"
             "в) <продолжить сбор ссылок> - eсли произошло превывание "
             "программы при сборе ссылок\n"
             "г) <продолжить обработку ссылок> - eсли  произошло "
             "прерывание при обработке ссылок\n")

question_2 = ('Так же введите количество сохраненных ссылок'
              ' до прерывания (см. Журнал)\n')

question_3 = ("Введите сферу, которую хотите обработать/продолжить..\n")

question_4 = "номер последнего обработанного города(см. Журнал)\n"

question_5 = ("Введите количество обработанных ссылок (см.Журнал)"
              " для продолжения обработки с того же места\n")


def counter(start=0):
    def number_plus():
        nonlocal start
        start += 1
        return start
    return number_plus


def сreate_excel_tables():
    headers = ['id_компании', 'Тип партнёра (мастер/компания)',
               'Имя', 'Фамилия', 'Телефон', 'Email', 'Адрес', 'О себе',
               'instagram', 'telegram', 'whatsapp', 'youtube', 'vk',
               'Личный сайт', 'odnoklassniki', 'Логотип', 'Широта',
               'Долгота', 'URL фотографий рабочего места, через |']
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    wb.save("data/partners.xlsx")
    wb.close()
    headers = ['Id мастера', 'Имя клиента', 'Рейтинг', 'Дата', 'Текст отзыва',
               'URL прикреплённых фотографий, через |']
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    wb.save("data/reviews.xlsx")
    wb.close()
    headers = ['Id партнёра', 'Название услуги',
               'Цена, руб', 'Длительность, минут']
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    wb.save("data/services.xlsx")
    wb.close()


def append_data_table_partners(saving_list: list):
    try:
        wb = load_workbook("data/partners.xlsx")
        ws = wb.active
        ws.append(saving_list)
        wb.save("data/partners.xlsx")
    except Exception as ex:
        logger.warning(ex)
    finally:
        wb.close()


def get_name_of_partner(soup) -> str:
    try:
        name = (soup.find("div", class_="sticky-wrapper _position_top _header"
                " _border_auto _wide").find("div", class_="orgpage"
                "-header-view__header-wrapper")
                .find("h1", class_="orgpage-header-view__header")).text
        return name
    except Exception:
        return None


def get_phone_number(soup) -> str:
    try:
        number = (soup.find("div", class_="orgpage-header-view__contacts")
                  .find("div", class_="orgpage-phone"
                        "s-view__phone-number").text)
        return number
    except Exception:
        return None


def get_address(soup) -> str:
    try:
        address = soup.find("a", class_="business"
                            "-contacts-view__address-link").text
        return address
    except Exception:
        return None


def get_messenger(soup, name_messanger: str) -> str:
    try:
        all_messangers = soup.find_all("a", class_="button _view_secondary"
                                       "-gray _ui _size_medium _link")
        for tag in all_messangers:
            if name_messanger in tag.get("aria-label"):
                return tag.get('href')
    except Exception:
        return None


def get_website(soup):
    try:
        website = soup.find("span", class_="business-urls-view__text").text
        return website
    except Exception:
        return None


def get_logo_link(soup):
    try:
        logo = soup.find('img', class_='img-with-alt').get('src')
        return logo
    except Exception:
        return None


def get_coordinates(driver):
    try:
        coordinates = (driver.current_url.split("/")[7].replace("?ll=", "")
                       .replace("%2C", " ").split("&")[0].split())
        return coordinates[0], coordinates[1]
    except Exception:
        return None


def get_photos_links(driver, link):
    try:
        list_of_photo_links = []
        driver.get(f'{link}gallery')
        sleep(1)
        scroll_down_photo_page(driver)
        soup = BeautifulSoup(driver.page_source, "lxml")
        blocks_of_photo = soup.find_all("div", class_="photo-list__"
                                        "frame-wrapper")
        if blocks_of_photo:
            for item in blocks_of_photo:
                try:
                    link = item.find("img").get("src")
                    list_of_photo_links.append(link)
                except Exception:
                    continue
        return " | ".join(list_of_photo_links)
    except Exception:
        return None


def get_all_reviews(soup):
    try:
        temp = 'business-reviews-card-view__reviews-container'
        all_reviews = (soup.find(class_=temp).find_all('div',
                       class_='business-reviews-card-view__review'))
        return all_reviews
    except Exception:
        return None


def get_name_client(soup):
    try:
        name = soup.find('span').text
        return name
    except Exception:
        return None


def get_rating(soup):
    try:
        rating = soup.find_all('span', class_='inline-image _loaded '
                               'business-rating-badge-view'
                               '__star _full _size_m')
        return len(rating)
    except Exception:
        return None


def get_date_review(soup):
    try:
        date = soup.find('span', class_='business-review-view__date').text
        return date
    except Exception:
        return None


def get_text_review(soup):
    try:
        text = soup.find('span', class_='business-review-view__body-text').text
        return text
    except Exception:
        return None


def get_all_serevices(soup):
    try:
        return soup.find_all('div', class_='business-'
                             'full-items-grouped-view__item _view_list')
    except Exception:
        return None


def get_name_service(soup):
    try:
        title = soup.find('div', class_='related-item-list-view__title').text
        return title
    except Exception:
        return None


def get_price(soup):
    try:
        price = soup.find('div', class_='related-item-list-view__price').text
        return price[:-1]
    except Exception:
        return None


def scroll_down_photo_page(driver):
    '''Scrolling down for all reviews seeing'''
    try:
        actions = ActionChains(driver)
        num_of_pushing_page_down = 25
        clickable_element = (driver.find_element(By.TAG_NAME,
                             "h1"))
        actions.click(clickable_element).perform()
        page_scrolling = driver.find_element(By.TAG_NAME, "body")
        for i in range(num_of_pushing_page_down):
            page_scrolling.send_keys(Keys.PAGE_DOWN)
            sleep(0.1)
    except Exception as ex:
        sleep(5)
        scroll_down_photo_page(driver)
        logger.warning(ex)


def scroll_page_down_reviews(driver):
    '''Scrolling down for all reviews seeing'''
    try:
        actions = ActionChains(driver)
        num_of_pushing_page_down = 20
        clickable_element = (driver.find_element(By.TAG_NAME,
                             "h1"))
        actions.click(clickable_element).perform()
        page_scrolling = driver.find_element(By.TAG_NAME, "body")
        for i in range(num_of_pushing_page_down):
            page_scrolling.send_keys(Keys.PAGE_DOWN)
            sleep(0.2)
    except Exception as ex:
        sleep(5)
        scroll_page_down_reviews(driver)
        logger.warning(ex)


def create_file_for_links():
    with open("data/links.txt", 'w') as file:
        file.write('')


def save_links_in_txt(list):
    with open("data/links.txt", 'a') as file:
        for link in list:
            file.write(f'{link}\n')
