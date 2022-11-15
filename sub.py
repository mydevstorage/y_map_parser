from bs4 import BeautifulSoup
# from loguru import logger
from openpyxl import Workbook, load_workbook
from time import sleep


DATA_FOLDER = '/home/roman/real_python/web_parsing/yandex_map_parser'


def counter(start=0):
    def number_plus():
        nonlocal start
        start += 1
        return start
    return number_plus


def сreate_excel_tables():
    headers = ['id_компании', 'Город', 'Название', 'Телефон', 'Адрес',
               'Сайт', 'WhatsApp', 'Telegram', 'Вконтакте', 'Viber',
               'Логотип', 'Широта', 'Долгота', 'Ссылки на фото']
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    wb.save(f"{DATA_FOLDER}/data/partners.xlsx")
    wb.close()
    headers = ['id_компании', 'Имя клиента', 'Рейтинг', 'Дата', 'Отзыв']
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    wb.save(f"{DATA_FOLDER}/data/reviews.xlsx")
    wb.close()
    headers = ['id_компании', 'Наименование услуги',
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
    name = (soup.find("div", class_="sticky-wrapper _position_top _header"
            " _border_auto _wide").find("div", class_="orgpage"
            "-header-view__header-wrapper")
            .find("h1", class_="orgpage-header-view__header")).text
    return name


def get_phone_number(soup) -> str:
    number = (soup.find("div", class_="orgpage-header-view__contacts")
              .find("div", class_="orgpage-phones-view__phone-number").text)
    return number


def get_address(soup) -> str:
    address = soup.find("a", class_="business"
                        "-contacts-view__address-link").text
    return address


# [viber vkontakte whatsapp telegram]
def get_messenger(soup, name_messanger: str) -> str:

    all_messangers = soup.find_all("a", class_="button _view_secondary"
                                   "-gray _ui _size_medium _link")
    for tag in all_messangers:
        if name_messanger in tag.get("aria-label"):
            return tag.get('href')


def get_website(soup):
    website = soup.find("span", class_="business-urls-view__text").text
    return website


def get_logo_link(soup):
    logo = soup.find('img', class_='img-with-alt').get('src')
    return logo


def get_coordinates(driver):
    coordinates = (driver.current_url.split("/")[7].replace("?ll=", "")
                   .replace("%2C", " ").split("&")[0].split())
    return coordinates[0], coordinates[1]


def ger_photos_links(driver, link):
    list_of_photo_links = []
    driver.get(f'{link}gallery')
    sleep(1)
    soup = BeautifulSoup(driver.page_source, "lxml")
    blocks_of_photo = soup.find_all("div", class_="photo-list__frame-wrapper")
    for item in blocks_of_photo:
        try:
            link = item.find("img").get("src")
        except Exception:
            break
        list_of_photo_links.append(link)
    return ", ".join(list_of_photo_links)


def get_all_reviews(soup):
    temp = 'business-reviews-card-view__reviews-container'
    all_reviews = (soup.find(class_=temp).find_all('div',
                   class_='business-reviews-card-view__review'))
    return all_reviews


def get_name_client(soup):
    name = soup.find('span').text
    return name


def get_rating(soup):
    rating = soup.find_all('span', class_='inline-image _loaded '
                           'business-rating-badge-view__star _full _size_m')
    return len(rating)


def get_date_review(soup):
    date = soup.find('span', class_='business-review-view__date').text
    return date


def get_text_review(soup):
    text = soup.find('span', class_='business-review-view__body-text').text
    return text


def get_all_serevices(soup):
    return soup.find_all('div', class_='business-'
                         'full-items-grouped-view__item _view_list')


def get_name_service(soup):
    title = soup.find('div', class_='related-item-list-view__title').text
    return title


def get_price(soup):
    price = soup.find('div', class_='related-item-list-view__price').text
    return price
