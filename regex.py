import re

file = "/home/lisen/workspace/phpbot/my.txt"

read = open(file, mode="r")
string = read.read()


def findAddress(string):
    res = re.findall(r'<td>Address</td>(?:.*?)<td>(.*?)<a', string, flags=re.S)
    res = res[0].replace('\n', '').replace('\r', '').strip()
    return {'Address':res}

def findPublicKey(string):
    res = re.findall(r'<td>Public key</td>(?:.*?)<td>(.*?)</td>', string, flags=re.S)
    res = res[0].replace('\n', '').replace('\r', '').strip()
    print(res)
    return res

findPublicKey(string)



# dict = {}
# res = re.findall(r'<table class="table table-sm table-striped">(.*?)</table>', string,flags=re.S)
# head = res[0]
# # print(head)
# for tr in re.findall(r'<tr>(.*?)</tr>', head,flags=re.S):
#     td = re.findall(r'<td>(.*?)</td>', tr,flags=re.S)
#     if td :
#         dict[td[0]] = td[1]
    
# for it in dict.keys():
#     print(it)
#     print(dict[it])

