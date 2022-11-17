from bs4 import BeautifulSoup
# from loguru import logger
from openpyxl import Workbook, load_workbook
from time import sleep


DATA_FOLDER = '/home/roman/real_python/web_parsing/yandex_map_parser'


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
             "а) <Название города> - для анализа по одному городу,\n"
             "б) Слово <Все>' - для анализа всех городов России "
             "с населением более 100 тысяч человек...\n"
             "в) Если произошло превывание программы при сборе ссылок"
             ", введите <продолжить сбор ссылок>\n"
             "г) Если  произошло прерывание при обработке ссылок,"
             " введите <продолжить обработку ссылок>")

question_2 = ('Так же введите количество сохраненных ссылок'
              ' до прерывания (см. Журнал)\n')

question_3 = ("Введите сферу, которую хотите обработать/продолжить..\n")

question_4 = "номер последнего обработанного города(см. Журнал)\n"

question_5 = ("количество обработанных ссылок (см.Журнал)\n"
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
    wb.save(f"{DATA_FOLDER}/data/partners.xlsx")
    wb.close()
    headers = ['Id мастера', 'Имя клиента', 'Рейтинг', 'Дата', 'Текст отзыва',
               'URL прикреплённых фотографий, через |']
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    wb.save(f"{DATA_FOLDER}/data/reviews.xlsx")
    wb.close()
    headers = ['Id партнёра', 'Название услуги',
               'Цена, руб', 'Длительность, минут']
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    wb.save(f"{DATA_FOLDER}/data/services.xlsx")
    wb.close()


def append_data_table_partners(saving_list: list):

    wb = load_workbook(f"{DATA_FOLDER}/data/partners.xlsx")
    ws = wb.active
    ws.append(saving_list)
    wb.save(f"{DATA_FOLDER}/data/partners.xlsx")


def append_data_table_reviews(saving_list: list):

    wb = load_workbook(f"{DATA_FOLDER}/data/reviews.xlsx")
    ws = wb.active
    ws.append(saving_list)
    wb.save(f"{DATA_FOLDER}/data/reviews.xlsx")


def append_data_table_services(saving_list: list):

    wb = load_workbook(f"{DATA_FOLDER}/data/services.xlsx")
    ws = wb.active
    ws.append(saving_list)
    wb.save(f"{DATA_FOLDER}/data/services.xlsx")


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


def ger_photos_links(driver, link):
    try:
        list_of_photo_links = []
        driver.get(f'{link}gallery')
        sleep(1)
        soup = BeautifulSoup(driver.page_source, "lxml")
        blocks_of_photo = soup.find_all("div", class_="photo-list__"
                                        "frame-wrapper")
        for item in blocks_of_photo:
            try:
                link = item.find("img").get("src")
            except Exception:
                break
            list_of_photo_links.append(link)
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
        return price
    except Exception:
        return None
