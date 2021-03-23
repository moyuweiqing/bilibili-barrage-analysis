import json
import pandas as pd
import time
import requests
import os
import re

info_table = pd.DataFrame(columns=['uid', 'follower'])
row_cnt = 1

def get_fs(url):
    global info_table, row_cnt

    res = requests.get(url)
    rep = json.loads(res.text)
    alist = []
    alist.append(rep['data']['mid'])
    alist.append(rep['data']['follower'])
    info_table.loc[row_cnt] = alist
    row_cnt += 1
    info_table.to_csv('up主粉丝数.csv', encoding='gb18030')

if __name__ == '__main__':
    uplist = []

    filenames = os.listdir('./源数据/')  # 设定调用文件的相对路径
    f = []
    for i in filenames:
        if '.csv' in str(i):
            f.append(i)
    for i in f:
        data = pd.read_csv('./源数据/' + i, encoding = 'gb18030')
        for j in data['up主id']:
            if j in uplist:
                continue
            else:
                uplist.append(j)
                url = 'https://api.bilibili.com/x/relation/stat?vmid=' + str(j) + '&jsonp=jsonp'
                get_fs(url)
                print('finished', j)