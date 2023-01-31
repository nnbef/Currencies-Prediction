from RowFromTable import RowFromTable
from datetime import date as dtdate
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import argparse


class URLBuilder:
    def __init__(self, currency, start_date):
        currency_dict = {'usd': '1235', 'eur': '1239'}
        currency = currency if currency.isdigit() else currency_dict[currency.lower()]
        current_date = datetime.now()
        current_date = f'{current_date.day}.{current_date.month}.{current_date.year}'
        self.__url = 'https://www.cbr.ru/currency_base/dynamics/'
        self.__url += '?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1'
        self.__url += '&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R0'
        self.__url += currency
        self.__url += '&UniDbQuery.From=' + start_date
        self.__url += '&UniDbQuery.To=' + current_date

    def get_url(self):
        return self.__url


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--startDate', default='01.01.2005')
    parser.add_argument('--currency', default='USD')
    parser.add_argument('--fileName',
                        default=f'ParseFile {datetime.now().day}.{datetime.now().month}.{datetime.now().year}')
    parser.add_argument('--format', default='csv')
    parser.add_argument('--useFile', default=False)
    parser.add_argument('--split', default=0.8)
    return parser


def parse(start_date, currency):
    print('Start of parsing')
    try:
        url_builder = URLBuilder(currency, start_date)
        page = requests.get(url_builder.get_url())
        bs = BeautifulSoup(page.text, "lxml")
        table = bs.find('table', 'data')

        print('Currency:', table.find('td').get_text().replace('\n', ''))
        data = []
        rows = table.find_all('td')

        print('\tStart cleaning table')
        clear_rows = []
        for row in rows:
            try:
                date = row.get_text().split('.')
                date.reverse()
                dtdate.fromisoformat('-'.join(date))
                clear_rows.append(row)
                continue
            except Exception:
                pass
            try:
                int(row.get_text())
                clear_rows.append(row)
                continue
            except Exception:
                pass
            try:
                float(row.get_text().replace(',', '.'))
                clear_rows.append(row)
                continue
            except Exception:
                pass
        rows = clear_rows
        print('\tCleaning table completed successfully')

        for i in range(-1, -len(rows), -3):
            data.append(RowFromTable(rows[i-2], rows[i-1], rows[i]))
    except Exception:
        print("Failed to parse site")
        exit()
    else:
        print('Parsing completed successfully')
        return data
