import csv

import requests
import re
import json


# 获取弹幕内容
def get_content(page, cid):
    url = 'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid={}&pid=40112794&segment_index={}'.format(cid, page)
    headers = {
        "authority": "api.bilibili.com",
        "method": "GET",
        "path": "/x/v2/dm/web/seg.so?type=1&oid={}&pid=40112794&segment_index={}".format(cid, page),
        "scheme": "https",
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "buvid3=3B61288D-B886-6198-5112-1F705E7EB43369808infoc; CURRENT_FNVAL=80; _uuid=BBC2D6F3-BB14-2900-4B78-43D4A194BEBF50856infoc; blackside_state=1; sid=7w15wel6; rpdid=|(JYlmuluumR0J'uYkRkR||l); Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1624240436; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1624240436; PVID=2; bfe_id=5db70a86bd1cbe8a88817507134f7bb5",
        "origin": "https://www.bilibili.com",
        "referer": "https://www.bilibili.com/video/av40112794/",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",

    }
    r = requests.get(url=url, headers=headers).text
    return r


# 正则表达式匹配弹幕内容
def get_data(r):
    data_list = re.findall(':(.*?)@', r)
    with open('danmu.csv', 'a', encoding='gb18030', newline='')as f:
        writer = csv.writer(f)
        if len(data_list) > 0:
            for data in data_list:
                writer.writerow([data])

# 获取弹幕cid
# bvid_list为所需要爬取的视频的BV号
def get_cid():
    bvid_list = ['BV1Dt411W7aL', 'BV1bW411i7uc', 'BV13x411q7Dz', 'BV17W411z7xA']
    for bvid in bvid_list:
        url = 'https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(bvid)
        headers = {
            "authority": "api.bilibili.com",
            "method": "GET",
            "path": "/x/player/pagelist?bvid=BV1bW411i7uc&jsonp=jsonp",
            "scheme": "https",
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "buvid3=3B61288D-B886-6198-5112-1F705E7EB43369808infoc; CURRENT_FNVAL=80; _uuid=BBC2D6F3-BB14-2900-4B78-43D4A194BEBF50856infoc; blackside_state=1; sid=7w15wel6; rpdid=|(JYlmuluumR0J'uYkRkR||l); Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1624240436; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1624240436; bfe_id=5db70a86bd1cbe8a88817507134f7bb5; PVID=4",
            "origin": "https://www.bilibili.com",
            "referer": "https://www.bilibili.com/video/av18089528/?spm_id_from=333.788.b_765f64657363.2",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
        }
        r = requests.get(url=url, headers=headers).text
        cid_list = []
        dictr = json.loads(r)
        data_list = dictr['data']
        for data in data_list:
            cid = data['cid']
            cid_list.append(cid)
        return cid_list


def main():
    cid_list = get_cid()
    for cid in cid_list:
        for page in range(1, 20):
            r = get_content(page, cid)
            get_data(r)


if __name__ == '__main__':
    main()
