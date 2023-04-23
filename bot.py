import os
import requests
from bs4 import BeautifulSoup

import datetime

phpurl = "https://main1.phpcoin.net/apps/explorer/"


def pares(file):
    def header(soup):
        item = {}
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            if tds[1].string:
                value = tds[1].string
                value = value[:value.find(' (')]
                item[tds[0].string] = value
            else:
                item[tds[0].string] = tds[1].next_element

            item[tds[0].string] = item[tds[0].string].replace(
                '\n', '').replace('\r', '').strip()
        return item

    def body(soup):
        items = []
        keys = []
        tr = soup.find('thead').find('tr')
        for td in soup.find('thead').find('tr').find_all('th'):
            keys.append(td.string)

        for tr in soup.find('tbody').find_all('tr'):
            item = {}
            for key, td in zip(keys, tr.find_all('td')):
                if td.string:
                    item[key] = td.string
                elif td.find('a') and td.find('a').find('span'):
                    item[key] = td.find('a').find('span').string
                elif td.next:
                    item[key] = td.next
                    if td.find('span'):
                        item[key] = item[key] + td.find('span').string

                else:
                    item[key] = " "
                item[key] = item[key].replace(
                    '\n', '').replace('\r', '').strip()
                item[key] = ' '.join(item[key].split())
            items.append(item)
        return items

    soup = BeautifulSoup(file, 'html.parser')
    table = soup.find_all('table')
    headcontent = header(table[0])
    bodycontent = body(table[1])
    return [headcontent, bodycontent]


def culclation(items):
    now = datetime.datetime.now()
    end = now
    start = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond)
    print(now)
    print(start)
    print(end)
    income = {}
    for item in items:
        time = datetime.datetime.strptime(item['Date'], '%Y-%m-%d %H:%M:%S')
        if (start <= time <= end):
            if item['Type'] in income.keys():
                income[item['Type']] = income[item['Type']] + \
                    float(item['Value'])
            else:
                income[item['Type']] = float(item['Value'])
    return income


def fetch(address):
    result = requests.get(
        "https://main1.phpcoin.net/apps/explorer/address.php?address=" + address)
    if result.status_code == 200:
        return result.text


def dailyIncom(address):
    file = fetch(address)
    for i in range(5):
        if file:
            break
        file = fetch(address)
        slepp(10)
    document = pares(file)
    income = culclation(document[1])
    return income


address = "Pst5VEoCwbeowUoEPLc4iQQvgVKJqSJi3N"
print(dailyIncom(address))
