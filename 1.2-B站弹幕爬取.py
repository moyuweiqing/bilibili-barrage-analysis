# coding=utf-8
import requests
import pandas as pd
from lxml import etree
import re
import time

class BiliSpider:
    def __init__(self,BV):
        # 构造要爬取的视频url地址
        self.BV = BV
        self.BVurl = "https://m.bilibili.com/video/"+BV
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Mobile Safari/537.36"}
        self.info_table = pd.DataFrame(columns=['弹幕'])
        self.row_cnt = 1

    # 弹幕都是在一个url请求中，该url请求在视频url的js脚本中构造
    def getXml_url(self):
        # 获取该视频网页的内容
        response = requests.get(self.BVurl, headers = self.headers)
        html_str = response.content.decode()

        # 使用正则找出该弹幕地址
        # 格式为：https://comment.bilibili.com/168087953.xml
        # 我们分隔出的是地址中的弹幕文件名，即 168087953
        getWord_url = re.findall("cid:(.*?),", html_str)
        getWord_url = getWord_url[0].replace("+","").replace(" ","")
        # 组装成要请求的xml地址
        xml_url = "https://comment.bilibili.com/{}.xml".format(getWord_url)
        return xml_url

    # Xpath不能解析指明编码格式的字符串，所以此处我们不解码，还是二进制文本
    def parse_url(self,url):
        response = requests.get(url,headers = self.headers)
        return response.content

    # 弹幕包含在xml中的<d></d>中，取出即可
    def get_word_list(self,str):
        html = etree.HTML(str)
        word_list = html.xpath("//d/text()")
        return word_list

    def run(self):
        # 1.根据BV号获取弹幕的地址
        start_url = self.getXml_url()
        # 2.请求并解析数据
        xml_str = self.parse_url(start_url)
        word_list = self.get_word_list(xml_str)
        # 3.打印
        for word in word_list:
            alist = []
            alist.append(word)
            self.info_table.loc[self.row_cnt] = alist
            self.row_cnt += 1
        self.info_table.to_csv('./弹幕/职业职场/' + self.BV + '.csv', encoding='gb18030')

if __name__ == '__main__':
    file = pd.read_csv('./源数据/职业职场.csv', encoding = 'gb18030')
    for i in file['BV号']:
        spider = BiliSpider(i)
        spider.run()
        # time.sleep(1)
        print('finished', i)