import os
import requests
from bs4 import BeautifulSoup
import time
import datetime
import transaction as tran

phpurl = "https://main1.phpcoin.net/apps/explorer/address.php?address="


class Network:
    def __init__(self, url) -> None:
        self.Url = url

    def fetchData(self, address):
        wallet = self.fetchDataAddressData(address)
        wallet.Transactions = self.fetchDataTransactionData(address)
        return wallet

    def fetchWeb(self, address):
        result = requests.get(phpurl + address)
        if result.url != self.Url + address:
            return False, "your address is wrong"
        if result.status_code == 200:
            return True, result.text

    def fetchDataAddressData(self, address):
        ret, text = self.fetchWeb(address=address)
        if ret == False:
            return ret, text
        soup = BeautifulSoup(text, 'html.parser')
        for link in soup.find_all('a'):
            link.decompose()
        table = soup.find_all('table')
        if not isinstance(table, list) or len(table) != 2:
            return False, "something wrong"
        table = table[0]

        wallet = tran.Wallet()
        items = []
        for tr in soup.find_all('tr')[:5]:
            td = tr.find_all('td')[1]
            if td.string:
                items.append(td.string)
            else:
                items.append(td.text)
        wallet.Address = items[0].strip()
        wallet.Public = items[1].strip()
        items[2] = items[2].strip()
        wallet.Received = float(items[2][:items[2].find('(')])
        items[3] = items[3].strip()
        wallet.Sent = float(items[3][:items[3].find('(')])
        wallet.Balance = float(items[4].strip())
        return wallet

    def fetchDataTransactionData(self, address):
        ret, text = self.fetchWeb(address=address)
        if ret == False:
            return ret, text
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find_all('table')
        if not isinstance(table, list) or len(table) != 2:
            return False, "something wrong"

        table = table[1]

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
        trans = []
        for item in items:
            tra = tran.Transaction()
            tra.Id = item['Id']
            tra.Date = datetime.datetime.strptime(
                item['Date'], '%Y-%m-%d %H:%M:%S')
            tra.Height = int(item['Height'])
            tra.Block = item['Block']
            tra.Type = item['Type']
            tra.Value = float(item['Value'])
            tra.Fee = item['Fee']
            if tra.Value > 0:
                tra.From = item['From/To']
            else:
                tra.To = item['From/To']
            trans.append(tra)
            # print(tra.toJion())
        return trans


network = Network(
    "https://main1.phpcoin.net/apps/explorer/address.php?address=")
network.fetchDataTransactionData("Pst5VEoCwbeowUoEPLc4iQQvgVKJqSJi3N")
