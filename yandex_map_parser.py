import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
import random
from loguru import logger
import argparse

logger.add('log.log', format="[{time:HH:mm:ss}] {level} {message} ",
           level="DEBUG",
           rotation='30 MB', compression='zip', retention=None)

DATA_FOLDER = '/home/roman/real_python/web_parsing/yandex_map_parser'

PATH_TO_CHROME_DRIVER = ("/home/roman/real_python/web_parsing/"
                         "venchur_funds_parser/chrome_ driver/chromedriver")

user_agent = ("user-agent=Mozilla/5.0 (X11; Linux x86_64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/106.0.0.0 Safari/537.36")

def get_options():
    ''' Parse the arguments in the command line'''

    parser = argparse.ArgumentParser()
    HELP_INFO1 = 'choose and type [csv, excel ,db] for writing method'
    HELP_INFO2 = 'choose and type [chrome, firefox] for browser tool'

    parser.add_argument('output_format', choices=['csv', 'excel', 'sqlite3'],
                        help=HELP_INFO1)
    parser.add_argument('browser', choices=['chrome',
                        'firefox'], help=HELP_INFO2)
    return parser.parse_args()


def get_driver_chrome():

    options = webdriver.ChromeOptions()
    options.add_argument(user_agent)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.headless = True
    driver = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER,
                            options=options)
    return driver

def get_all_links():
    '''Downloads all links and writes it in a file '''

    headers = {"accept": "text/css,*/*;q=0.1",
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/106.0.0.0 Safari/537.36'}

    for page in range(0, AMOUNT_OF_FUNDS_FOR_PARSING, STEP):
        try:
            fund_links = {}
            gfs = requests.get(f"https://project-valentine-api.herokuapp.com/"
                               f"investors?page%5Blimit%5D="
                               f"10&page%5Boffset%5D={page}", headers=headers)
            s = gfs.json()
            for i in s['data']:
                temp = (f"https://connect.visible.vc/investors/"
                        f"{i['attributes']['slug']}")
                name = i['attributes']['name']
                fund_links[name] = temp

            if not os.path.exists(f"{DATA_FOLDER}/data"):
                os.mkdir(f"{DATA_FOLDER}/data")

            with open(f"{DATA_FOLDER}/data/all_links_{page}.json", "w") as f:
                json.dump(fund_links, f, indent=4, ensure_ascii=False)
            time.sleep(random.randint(1, 2))

            logger.debug(f'{page + 10} links are got')
        except Exception:
            logger.warning(f'offset number {page} was not loaded')

def append_data_to_excel(main_row_for_table):

    del main_row_for_table[0]
    wb = load_workbook(f"{DATA_FOLDER}/result.xlsx")
    ws = wb.active
    ws.append(main_row_for_table)
    wb.save(f"{DATA_FOLDER}/result.xlsx")

def create_headers_in_excel_table():

    wb = Workbook()
    ws = wb.active
    ws.append(HEADERS_RESULT_TABLE)
    wb.save(f"{DATA_FOLDER}/result.xlsx")
    wb.close()


@logger.catch()   
def main():

    outer_args = get_options()

    create_headers_in_excel_table()
 
    get_all_links()
    
    treatment_of_data_with_browser(outer_args)


if __name__ == '__main__':
    main()