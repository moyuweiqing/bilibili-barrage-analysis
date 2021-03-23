from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re

judge = True
row_cnt = 1

def parse(driver):
    global judge, row_cnt

    info_table = pd.DataFrame(
        columns=['href', '时长', '名称', 'BV号', '播放量', '弹幕数', 'up主'])
    row_cnt = 1
    try:
        href_list = []
        bv_list = []
        for row in range(1, 21):
            href_xpath = '//*[@id="videolist_box"]/div[2]/ul/li[' + str(row) + ']/div/div[1]/div/a'

            href = driver.find_element_by_xpath(href_xpath).get_attribute('href')
            bv = str(href).split('/')[-1]

            href_list.append(href)
            bv_list.append(bv)

        timelist, titlelist, playslist, uplist = parse2(driver)

        for i in range(0, 20):
            alist = []
            alist.append(href_list[i])
            alist.append(timelist[i])
            alist.append(titlelist[i])
            alist.append(bv_list[i])
            alist.append(playslist[2 * i])
            alist.append(playslist[2 * i + 1])
            alist.append(uplist[i])

            info_table.loc[row_cnt] = alist
            row_cnt += 1

        if judge:
            info_table.to_csv('./data/科学科普.csv', mode='a+', index=False, header=True, encoding = 'gb18030')
            judge = False
        else:
            info_table.to_csv('./data/科学科普.csv', mode='a+', index=False, header=False, encoding='gb18030')
    except Exception as e:
        print(e)

def parse2(driver):
    html_text = bs(driver.page_source, 'lxml')
    video_list = html_text.find_all('div', class_ = 'video-list list-c')[0]

    dtimes = video_list.find_all('span', class_ = 'dur')
    timelist = []
    for i in dtimes:
        timelist.append(re.findall(">(.*?)<", str(i))[0])

    titles = video_list.find_all('p', class_ = 't')
    titlelist = []
    for i in titles:
        titlelist.append(re.findall('>(.*?)<', str(i))[0])

    plays = video_list.find_all('span', class_ = 'v-info-i')
    playslist = []
    for i in plays:
        playslist.append(re.findall("span>(.*?)</span", str(i))[0])

    ups = video_list.find_all("div", class_= 'up-info')
    uplist = []
    for i in ups:
        uplist.append(re.findall('title="(.*?)"', str(i))[0])

    return timelist, titlelist, playslist, uplist

if __name__ == '__main__':
    date = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = r'D:\360极速浏览器下载\chromedriver_win32_88\chromedriver.exe'
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

    for page in range(1, 7):
        url = 'https://www.bilibili.com/v/technology/science/#/all/click/0/' + str(page) + '/2021-01-01,2021-02-28'
        driver.get(url)
        time.sleep(3)
        parse(driver)
        print('finished', page)