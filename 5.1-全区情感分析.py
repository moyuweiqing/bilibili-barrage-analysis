from snownlp import SnowNLP
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import jieba

def build_sentimental_analysis(file_name):

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

    plt.hist(sentimental_list, bins=np.arange(0, 1, 0.01), facecolor='g')
    plt.xlabel('Sentiments Probability')
    plt.ylabel('Quantity')
    plt.title('Analysis of Sentiments')
    # plt.show()
    plt.savefig('全区视频弹幕情感分析.png')

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