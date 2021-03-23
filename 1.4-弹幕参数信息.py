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
        self.info_table = pd.DataFrame(columns=['弹幕出现时间', '弹幕模式', '弹幕字体大小', '弹幕十六进制颜色', '弹幕池(0为普通池，1为字幕池，2为特殊池)', '弹幕发送者加密id', '弹幕id', '弹幕内容'])
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
        return response.content, response.text

    # 弹幕包含在xml中的<d></d>中，取出即可
    def get_word_list(self,str):
        html = etree.HTML(str)
        word_list = html.xpath("//d/text()")
        return word_list

    def get_info_list(self, html):
        info = re.findall('p="(.*?)"', html)
        return info

    def run(self):
        # 1.根据BV号获取弹幕的地址
        start_url = self.getXml_url()
        # 2.请求并解析数据
        xml_str, xml_text = self.parse_url(start_url)
        word_list = self.get_word_list(xml_str)
        word_list2 = self.get_info_list(xml_text)
        # 3.打印
        for i in range(0, len(word_list)):
            if len(word_list2[i]) < 8:
                continue
            alist = []
            tmplist = word_list2[i].split(',')

            alist.append(tmplist[0])  # 弹幕出现时间

            # 弹幕模型
            if str(tmplist[1]) in ['1', '2', '3']:
                alist.append('滚动弹幕')
            elif str(tmplist[1]) == '4':
                alist.append('底端弹幕')
            elif str(tmplist[1]) == '5':
                alist.append('顶端弹幕')
            elif str(tmplist[1]) == '6':
                alist.append('逆向弹幕')
            else:
                alist.append('特殊弹幕')

            alist.append(tmplist[2])  # 弹幕字体大小

            alist.append(str(hex(eval(str(tmplist[3])))))  # 弹幕十六进制颜色
            alist.append(tmplist[5])  # 弹幕池
            alist.append(tmplist[6])  # 用户id
            alist.append(tmplist[7])  # 弹幕id
            alist.append(word_list[i])
            self.info_table.loc[self.row_cnt] = alist
            self.row_cnt += 1

        self.info_table.to_csv('./弹幕(详细)/校园学习/' + self.BV + '.csv', encoding='gb18030')

if __name__ == '__main__':
    file = pd.read_csv('./源数据/校园学习.csv', encoding = 'gb18030')
    # i = 'BV1GW411g7mc'
    # spider = BiliSpider(i)
    # spider.run()
    for i in file['BV号']:
        try:
            spider = BiliSpider(i)
            spider.run()
            print('finished', i)
        except:
            continue
            # time.sleep(1)