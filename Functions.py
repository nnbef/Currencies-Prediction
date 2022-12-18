from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import argparse
import yaml


def ArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--startDate', default='01.01.2005')
    parser.add_argument('--currency', default='USD')
    parser.add_argument('--outputFile',
                        default=f'ParseFile {datetime.now().day}.{datetime.now().month}.{datetime.now().year}')
    parser.add_argument('--format', default='csv')
    return parser


def Parse(startDate, currency):
    currencyDict = {'usd': '1235', 'eur': '1239'}
    currentDate = datetime.now()
    currentDate = f'{currentDate.day}.{currentDate.month}.{currentDate.year}'
    url = f'https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1' \
          f'&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R0' \
          f'{currencyDict[currency.lower()]}&UniDbQuery.From={startDate}&UniDbQuery.To={currentDate}'

    page = requests.get(url)
    bs = BeautifulSoup(page.text, "lxml")
    table = bs.find('table', 'data')

    data = []
    rows = table.find_all('td')
    for i in range(-1, -len(rows), -3):
        data.append([rows[i - 2].get_text(), int(rows[i - 1].get_text()), float(rows[i].get_text().replace(',', '.'))])

    return data


def SaveData(data, outputFile, formatFile):
    if formatFile.lower() == 'yaml':
        with open(outputFile + '.yaml', 'w') as file:
            yaml.dump(data, file)
    elif formatFile.lower() == 'txt':
        with open(outputFile + '.txt', 'w') as file:
            for line in data:
                file.write('[')
                s = ''
                for elem in line:
                    s += str(elem) + ' '
                s = s.strip()
                file.write(s + ']\n')
    else:
        data = pd.DataFrame(data)
        if formatFile.lower() == 'json':
            data.to_json(outputFile + '.json')
        elif formatFile.lower() == 'xlsx':
            data.to_excel(outputFile + '.xlsx')
        elif formatFile.lower() == 'csv':
            data.to_csv(outputFile + '.csv')
        else:
            print('Failed to save file')
            return
    print('File saved successfully')
