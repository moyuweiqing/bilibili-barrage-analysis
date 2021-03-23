from snownlp import SnowNLP
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import jieba

def build_sentimental_analysis(file_name, dir):

    comment_list = []
    for i in file_name:
        file = pd.read_csv('./弹幕/' + i[0] + '/' + i[1] , encoding='gb18030')
        for j in file['弹幕']:
            comment_list.append(j)

    # 切词
    # word_list = word_cut(comment_list)

    #建立情感分析
    sentimental_list = []
    for i in comment_list:
        s = SnowNLP(i)
        sentimental_list.append(s.sentiments)

    avg = round(sum(sentimental_list) / len(sentimental_list), 4)
    plt.hist(sentimental_list, bins=np.arange(0, 1, 0.01), facecolor='g')
    plt.xlabel('Sentiments Probability')
    plt.ylabel('Quantity')
    plt.title('Analysis of Sentiments')
    # plt.show()
    plt.savefig('./情感分析/' + dir + '视频弹幕情感分析.png')
    return avg

def read_file():
    info_table = pd.DataFrame(columns=['频道', '平均情感指数'])
    row_cnt = 1
    dir_names = ['校园学习', '社科人文', '科学科普', '职业职场', '财经', '野生技术协会']
    for dir in dir_names:
        file_list = []
        files = os.listdir('./弹幕/' + dir + '/')
        for file in files:
            tmp = []
            tmp.append(dir)
            tmp.append(file)
            file_list.append(tmp)
        avg = build_sentimental_analysis(file_list, dir)
        print(avg)
        alist = []
        alist.append(dir)
        alist.append(avg)
        info_table.loc[row_cnt] = alist
        row_cnt += 1
    info_table.to_csv('各频道情感系数.csv', encoding='gb18030')

if __name__ == '__main__':
    read_file()