import pandas as pd
import jieba
import os
from wordcloud import WordCloud

def drawWordCloud(words, title, savepath='./results'): #定义一个词云绘制函数，通过词频绘制词云图并写出到特定目录
   path = os.path.abspath('..')
   if not os.path.exists(savepath):
      os.mkdir(savepath)
   wc = WordCloud(font_path='simkai.ttf',max_words=200, width=1920, height=1080, margin=5, background_color="white")#使用原先准备好的一张照片作为背景图
   wc.generate_from_frequencies(words)
   wc.to_file(os.path.join(savepath, title+'.png'))

def statistics(texts, stopwords):  #使用jieba库来进行分词，并统计词语出现次数
   words_dict = {}
   for text in texts:
      temp = jieba.cut(text, cut_all = True)
      for t in temp:
         if t in stopwords:
            continue
         if t in words_dict.keys():
            words_dict[t] += 1
         else:
            words_dict[t] = 1
   return words_dict

def save(words_dict1, savename, savapath):
   dict_list = list(words_dict1.keys())
   value_list = list(words_dict1.values())
   df = pd.DataFrame(columns=['词语', '次数'])
   row = 0
   for i in range(0, len(dict_list)):
      alist = []
      alist.append(dict_list[i])
      alist.append(value_list[i])
      df.loc[row] = alist
      row += 1
   df.to_csv(savapath + savename + '.csv', encoding='gb18030')

if __name__ == '__main__':
   stopwords = open('stopwords.txt', 'r', encoding='utf-8').read()
   dir_names = ['校园学习', '社科人文', '科学科普', '职业职场', '财经', '野生技术协会']
   for dir in dir_names:
      danmu = []
      filename = str(dir).split('.')[0]
      files = os.listdir('./弹幕/' + dir + '/')
      for file in files:
         data = pd.read_csv('./弹幕/' + dir + '/' + file, encoding='gb18030')
         for i in data['弹幕']:
            danmu.append(i)
      stopwords = open('stopwords.txt', 'r', encoding='utf-8').read()
      words_dict1 = statistics(danmu, stopwords)
      save(words_dict1, savename=filename + '词频表', savapath='./词频表/')
      drawWordCloud(words_dict1, filename + '词云图', savepath='./词云图/')