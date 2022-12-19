from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import argparse


def ArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--startDate', default='01.01.2005')
    parser.add_argument('--currency', default='USD')
    parser.add_argument('--outputFile',
                        default=f'ParseFile {datetime.now().day}.{datetime.now().month}.{datetime.now().year}')
    parser.add_argument('--format', default='csv')
    return parser


def Parse(startDate, currency):
    print('Start of parsing')
    currencyDict = {'usd': '1235', 'eur': '1239'}
    currency = currency if currency.isdigit() else currencyDict[currency.lower()]
    currentDate = datetime.now()
    currentDate = f'{currentDate.day}.{currentDate.month}.{currentDate.year}'
    try:
        url = 'https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1'
        url += '&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R0'
        url += currency
        url += '&UniDbQuery.From=' + startDate
        url += '&UniDbQuery.To=' + currentDate

        page = requests.get(url)
        bs = BeautifulSoup(page.text, "lxml")
        table = bs.find('table', 'data')

        print('Currency:', table.find('td').get_text().replace('\n', ''))
        data = []
        rows = table.find_all('td')

        print('\tStart cleaning table')
        clearRows = []
        for row in rows:
            try:
                x = pd.to_datetime(row.get_text(), dayfirst=True)
                clearRows.append(row)
                continue
            except Exception:
                pass
            try:
                x = int(row.get_text())
                clearRows.append(row)
                continue
            except Exception:
                pass
            try:
                x = float(row.get_text().replace(',', '.'))
                clearRows.append(row)
                continue
            except Exception:
                pass
        rows = clearRows
        print('\tCleaning table completed successfully')

        for i in range(-1, -len(rows), -3):
            data.append([pd.to_datetime(rows[i - 2].get_text(), dayfirst=True),
                         int(rows[i - 1].get_text()),
                         float(rows[i].get_text().replace(',', '.'))])
    except Exception:
        print("Failed to parse site")
        exit()
    else:
        print('Parsing completed successfully')
        return data
