from snownlp import SnowNLP
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import jieba

info_table = pd.DataFrame(columns=['BV号', '情感指数'])
row_cnt = 1

def build_sentimental_analysis(file_name):
    global info_table, row_cnt

    for i in file_name:
        comment_list = []
        file = pd.read_csv('./弹幕/' + i[0] + '/' + i[1] , encoding='gb18030')
        for j in file['弹幕']:
            comment_list.append(j)

        #建立情感分析
        sentimental_list = []
        for j in comment_list:
            s = SnowNLP(j)
            sentimental_list.append(s.sentiments)
        avg = round(sum(sentimental_list) / len(sentimental_list) , 4)
        alist = []
        alist.append(i[1])
        alist.append(avg)
        info_table.loc[row_cnt] = alist
        row_cnt += 1
        print('finished', i[0])
    info_table.to_csv('各视频弹幕情感分析.csv', encoding='gb18030')

def read_file():
    file_list = []
    dir_names = ['校园学习', '社科人文', '科学科普', '职业职场', '财经', '野生技术协会']
    for dir in dir_names:
        files = os.listdir('./弹幕/' + dir + '/')
        for file in files:
            tmp = []
            tmp.append(dir)
            tmp.append(file)
            file_list.append(tmp)
    build_sentimental_analysis(file_list)

if __name__ == '__main__':
    read_file()