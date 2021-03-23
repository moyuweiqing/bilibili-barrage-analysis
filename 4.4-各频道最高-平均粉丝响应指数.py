import pandas as pd
import os
import pyecharts.options as opts
from pyecharts.charts import Bar
import numpy as np


def draw_line(xlist, ylist, ylist2):
    c = (
        Bar(init_opts=opts.InitOpts(
            width='1800px',
            height='900px',
            js_host="./",
        ))
            .add_xaxis(xlist)
            .add_yaxis("视频平均粉丝响应指数", ylist)
            .add_yaxis("视频最高粉丝响应指数", ylist2)
            .set_global_opts(
            title_opts=opts.TitleOpts("各频道平均-最高粉丝响应指数"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
            .render('./柱状图/各频道平均-最高粉丝响应指数.html')
    )


if __name__ == '__main__':
    fansfile = pd.read_csv('up主粉丝数.csv', encoding='gb18030')
    dict_country = fansfile.set_index('uid').T.to_dict('list')

    xlist = []
    ylist = []
    ylist2 = []

    files = os.listdir('./源数据/')
    for file in files:
        numlist = []
        data = pd.read_csv('./源数据/' + file, encoding='gb18030')
        xlist.append(file.split('.')[0])
        for i in range(0, len(data)):
            a = dict_country[data['up主id'].iloc[i]][1]

            if '万' in str(data['播放量'].iloc[i]):
                b = int(float(str(data['播放量'].iloc[i]).split('万')[0]) * 10000)
            else:
                b = int(data['播放量'].iloc[i])

            c = round(b / a , 2)
            numlist.append(c)
        ylist.append(round(sum(numlist) / len(data) , 2))
        ylist2.append(max(numlist))

    draw_line(xlist, ylist, ylist2)