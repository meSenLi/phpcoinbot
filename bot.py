import os
import requests
from bs4 import BeautifulSoup

myurl = "https://main1.phpcoin.net/apps/explorer/address.php"
myaddress = "Pst5VEoCwbeowUoEPLc4iQQvgVKJqSJi3N"

def fun(url, address):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
    html=requests.post(url=url, headers=headers, data = {'address': address})
    print(html)
    return html.text

def parse(text):
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find('table').find_all('tbody')
    for data in table:
        rows = data.find_all('tr')
        print(rows)
        print("-----------------------------------")

parse(fun(myurl, myaddress))
    