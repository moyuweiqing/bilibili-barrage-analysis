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
            .add_yaxis("视频弹幕数", ylist)
            .set_global_opts(
            title_opts=opts.TitleOpts("知识区TOP10弹幕视频"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            brush_opts=opts.BrushOpts(),
        )
            .render('./柱状图/知识区TOP10弹幕视频.html')
    )


if __name__ == '__main__':
    namelist = []
    numlist = []
    files = os.listdir('./源数据/')
    for file in files:
        data = pd.read_csv('./源数据/' + file, encoding='gb18030')
        for i in range(0, len(data)):
            namelist.append(data['名称'].iloc[i])
            if '万' in str(data['弹幕数'].iloc[i]):
                numlist.append(int(float(str(data['弹幕数'].iloc[i]).split('万')[0]) * 10000))
            else:
                numlist.append(int(data['弹幕数'].iloc[i]))

    nnum = np.array(numlist)
    snum = np.argsort(nnum)

    xlist = []
    ylist = []
    for i in range(1, 11):
        xlist.append(namelist[snum[0 - i]])
        ylist.append(numlist[snum[0 - i]])
    draw_line(xlist, ylist)