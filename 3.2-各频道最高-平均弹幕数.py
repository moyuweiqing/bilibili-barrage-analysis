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
            .add_yaxis("视频平均弹幕数", ylist)
            .add_yaxis("视频最高弹幕数", ylist2)
            .set_global_opts(
            title_opts=opts.TitleOpts("各频道平均-最高弹幕数"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
            .render('./柱状图/各频道平均-最高弹幕数.html')
    )


if __name__ == '__main__':
    xlist = []
    ylist = []
    ylist2 = []

    files = os.listdir('./源数据/')
    for file in files:
        numlist = []
        data = pd.read_csv('./源数据/' + file, encoding='gb18030')
        xlist.append(file.split('.')[0])
        for i in range(0, len(data)):
            if '万' in str(data['弹幕数'].iloc[i]):
                numlist.append(int(float(str(data['弹幕数'].iloc[i]).split('万')[0]) * 10000))
            else:
                numlist.append(int(data['弹幕数'].iloc[i]))
        ylist.append(round(sum(numlist) / len(data) , 2))
        ylist2.append(max(numlist))

    draw_line(xlist, ylist, ylist2)