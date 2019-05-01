#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:26:28 2019

@author: seaswallow
"""

import os
from os import path
import numpy as np
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
from PIL import Image
from matplotlib import pyplot as plt
import random
import chardet
import jieba


################### 获取当前文件路径 ###############
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
################### 获取文本text ##################
text = open(path.join(d,'复联短评2.txt'),'rb').read()
text_charInfo = chardet.detect(text)
print(text_charInfo)

################## 中文编码需要改的地方 #############
{'encoding': 'gb18030', 'confidence': 1.0, 'language': ''}
text = open(path.join(d,r'复联短评2.txt'),encoding='gb18030',errors='ignore').read()
text+=' '.join(jieba.cut(text,cut_all=False)) # cut_all=False 表示采用精确模式

########  字体设置
font_path='Users/seaswallow/Documents/font/SourceHanSansCN-Regular.otf'
########  背景图片
background_Image = np.array(Image.open(path.join(d, "model3.jpg")))
########  提取背景图片颜色
img_colors = ImageColorGenerator(background_Image)

######## 自定义停词（不需要的词汇） ############
stopwords = set(STOPWORDS)
stopwords.update(['电影','一个','没有','自己','角色','这个','不是','就是','__','一场','什么','MCU','已经','作为'])
wc = WordCloud(
        font_path = font_path, # 中文需设置路径
        margin = 2, # 页面边缘
        mask = background_Image,
        scale = 2,
        max_words = 200, # 最多词个数
        min_font_size = 4, #
        stopwords = stopwords,
        random_state = 42,
        background_color = 'white', # 背景颜色
        # background_color = '#C3481A', # 背景颜色
        max_font_size = 150,
        )

wc.generate(text)
wc.recolor(color_func=img_colors)
#####  存储图像
wc.to_file('复联4.png')
#####  显示图像
plt.imshow(wc,interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.show()    

#获取文本词排序，可调整 stopwords
process_word = WordCloud.process_text(wc,text)
sort = sorted(process_word.items(),key=lambda e:e[1],reverse=True)
print(sort[:50]) # 获取文本词频最高的前50个词





## 黑白颜色渐变

def grey_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
         return "hsl(0, 0%%, %d%%)" % random.randint(50, 100)

# 随机设置hsl色值
wc.generate(text)        
wc.recolor(color_func=grey_color_func) 
plt.imshow(wc,interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.show()   