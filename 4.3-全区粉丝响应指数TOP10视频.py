import pandas as pd
import os
import pyecharts.options as opts
from pyecharts.charts import Bar
import numpy as np


def draw_line(xlist, ylist):
    c = (
        Bar(init_opts=opts.InitOpts(
            width='1800px',
            height='900px',
            js_host="./",
        ))
            .add_xaxis(xlist)
            .add_yaxis("粉丝响应指数", ylist)
            .set_global_opts(
            title_opts=opts.TitleOpts("知识区TOP10粉丝响应指数视频"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
            .render('./柱状图/知识区TOP10粉丝响应指数视频.html')
    )


if __name__ == '__main__':
    fansfile = pd.read_csv('up主粉丝数.csv', encoding='gb18030')
    dict_country = fansfile.set_index('uid').T.to_dict('list')

    namelist = []
    numlist = []
    files = os.listdir('./源数据/')
    for file in files:
        data = pd.read_csv('./源数据/' + file, encoding='gb18030')
        for i in range(0, len(data)):
            namelist.append(data['名称'].iloc[i])
            a = dict_country[data['up主id'].iloc[i]][1]

            if '万' in str(data['播放量'].iloc[i]):
                b = int(float(str(data['播放量'].iloc[i]).split('万')[0]) * 10000)
            else:
                b = int(data['播放量'].iloc[i])

            c = round(b / a , 2)
            numlist.append(c)

    nnum = np.array(numlist)
    snum = np.argsort(nnum)

    xlist = []
    ylist = []
    for i in range(1, 11):
        xlist.append(namelist[snum[0 - i]])
        ylist.append(numlist[snum[0 - i]])
    draw_line(xlist, ylist)