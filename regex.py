import re

file = "/workspaces/phpcoinbot/my.txt"

read = open(file, mode="r")
string = read.read()


def findAddress(string):
    res = re.findall(r'<td>Address</td>(?:.*?)<td>(.*?)<a', string, flags=re.S)
    res = res[0].replace('\n', '').replace('\r', '').strip()
    return {'Address': res}


def findPublicKey(string):
    res = re.findall(
        r'<td>Public key</td>(?:.*?)<td>(.*?)</td>', string, flags=re.S)
    res = res[0].replace('\n', '').replace('\r', '').strip()
    return {'Public key': res}


def findTatalReceived(string):
    res = re.findall(
        r'<td>Total received</td>(?:.*?)<td>(.*?)\((?:\d*)\)</td>', string, flags=re.S)
    res = res[0].replace('\n', '').replace('\r', '').strip()
    return {'Total received': res}


def findTotalSent(string):
    res = re.findall(
        r'<td>Total sent</td>(?:.*?)<td>(.*?)\((?:\d*)\)</td>', string, flags=re.S)
    res = res[0].replace('\n', '').replace('\r', '').strip()
    return {'Total received': res}


def findBalance(string):
    res = re.findall(
        r'<td(?:.*?)>Balance</td>(?:.*?)<td(?:.*?)>(.*?)</td>', string, flags=re.S)
    res = res[0].replace('\n', '').replace('\r', '').strip()
    print(res)
    return {'Balance': res}


def finditems(string):
    def retId(string):
        res = re.findall(r'(?:.*?)title="(.*?)">(?:.*?)', string, re.S)
        if res:
            return res[0]
        return ""

    def retDate(string):
        res = re.findall(r'(?:.*?)>(.*?)</span>(?:.*?)', string, re.S)
        if res:
            return res[0]
        return ""

    def retHeight(string):
        res = re.findall(r'(?:.*?)>(.*?)</a>(?:.*?)', string, re.S)
        if res:
            return res[0]
        return ""

    def retConf(string):
        return string

    def retBlock(string):
        res = re.findall(r'(?:.*?)title="(.*?)>(?:.*?)', string, re.S)
        if res:
            return res[0]
        return ""

    def retFromTo(string):
        res = re.findall(r'(?:.*?)title="(.*?)>(?:.*?)', string, re.S)
        if res:
            return res[0]
        return ""

    def retType(string):
        res = re.findall(r'(?:.*?)>(.*?)</span>(?:.*?)', string, re.S)
        if res:
            return res[0]
        return ""

    def retValue(string):
        # res = re.findall(r'(?:.*?)>(.*?)</span>(?:.*?)',string, re.S)
        return string

    def retFee(string):
        res = re.findall(r'(?:.*?)>(.*?)</span>(?:.*?)', string, re.S)
        if res:
            return res[0]
        return ""

    items = []
    string = re.findall(
        r'<tbody>(.*?)</tbody>', string, flags=re.S)[0]
    res = re.findall(r'<tr>(.*?)</tr>', string, re.S)

    print(len(res))
    for each in res:
        item = {}
        all = re.findall(r'<td(?:.*?)>(.*?)</td>', each, flags=re.S)
        item['Id'] = retId(all[0]).replace('\n', '').replace('\r', '').strip()
        item['Date'] = retDate(all[1]).replace(
            '\n', '').replace('\r', '').strip()
        item['Height'] = retHeight(all[2]).replace(
            '\n', '').replace('\r', '').strip()
        item['Conf'] = retConf(all[3]).replace(
            '\n', '').replace('\r', '').strip()
        item['Block'] = retBlock(all[4]).replace(
            '\n', '').replace('\r', '').strip()
        item['From/To'] = retFromTo(all[5]).replace('\n',
                                                    '').replace('\r', '').strip()
        item['Type'] = retType(all[6]).replace(
            '\n', '').replace('\r', '').strip()
        item['Value'] = retValue(all[7]).replace(
            '\n', '').replace('\r', '').strip()
        item['Fee'] = retFee(all[8]).replace(
            '\n', '').replace('\r', '').strip()
        items.append(item)
    return items


res = finditems(string)
