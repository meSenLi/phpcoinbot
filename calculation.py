import os
import requests
from bs4 import BeautifulSoup
import time
import datetime

phpurl = "https://main1.phpcoin.net/apps/explorer/address.php?address="


def pares(file):
    def header(soup):
        item = {}
        for tr in soup.find_all('tr'):
            if tr.find_all('td') == None:
                continue
            tds = tr.find_all('td')
            if len(tds) == 1:
                if tds[0].string:
                    item[tds[0].string] = 0
                continue
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
    # end = now - datetime.timedelta(hours=8)
    start = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                     microseconds=now.microsecond)
    start = start - datetime.timedelta(hours=8)
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


def culclationAvg(items):
    ret = {}
    times = []
    confs = []
    lasttime = None
    lastconf = None
    for item in items:
        if item['Type'] != 'Reward Masternode' and item['Type'] != 'Reward Stake':
            continue
        time = datetime.datetime.strptime(item['Date'], '%Y-%m-%d %H:%M:%S')
        conf = int(item['Conf'])
        if lasttime:
            times.append(lasttime - time)
            confs.append(conf - lastconf)
        lasttime = time
        lastconf = conf

    def average(numb=len(times)):
        ave = datetime.timedelta(0, 0, 0)
        aveconf = 0
        for time, conf in zip(times[:numb], confs[:numb]):
            ave = ave + time
            aveconf = aveconf + conf
        minutes = int(ave.total_seconds()//numb)//60
        hours = minutes//60
        minutes = minutes - hours*60
        ret[str(numb) + 'Time'] = datetime.time(hour=hours,
                                                minute=minutes, second=0).strftime("%H:%M")
        ret[str(numb) + 'Conf'] = aveconf//numb

    average(5)
    average(10)
    average()
    return ret


def fetch(address):
    result = requests.get(
        phpurl + address)
    if result.url == "https://main1.phpcoin.net/apps/explorer/":
        return None
    if result.status_code == 200:
        return result.text
    return None


def dailyIncom(address):
    file = fetch(address)
    for i in range(5):
        if file:
            break
        file = fetch(address)
        time.sleep(1)
    if file == None:
        return "Your address is wrong~"
    document = pares(file)
    data = culclation(document[1])
    data.update(culclationAvg(document[1]))
    return data


def calculation(addresses=None):
    if not (isinstance(addresses, str) or not addresses):
        addresses = "efaefaef"
    if addresses == None:
        addresses = ["Pst5VEoCwbeowUoEPLc4iQQvgVKJqSJi3N", "PbyMrPqPKW7rsWgRUKoAsxi56MVan8JVod",
                     "PaNPX1HHMNjLZEYkrDH5nrtW2xjkz7aGnX", "PoAayrZyMWnT3HpnKXRkUJMpApuPsM6rwN",
                     "PnLVEpcdmEtvzyQ31Z42LH7N92K2HVosVw", "PgxEExSE8kBavAvh2SHUy6WMCeJPsPyPE7",
                     "PhQmzQzv4EvH1jSE5xpggbD1n7ASazaYia"]
    result = {}
    if isinstance(addresses, str):
        addresses = [addresses]
    for address in addresses:
        result[address] = dailyIncom(address)
        print(dailyIncom(address))
    return result
