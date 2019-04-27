#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 20:34:03 2019

@author: seaswallow
"""

import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl  #用于修改 x 轴坐标

import os

from matplotlib.font_manager import _rebuild
_rebuild()




plt.rcParams['font.sans-serif'] = ['Simhei'] 
plt.rcParams['font.family']='sans-serif'
#解决负号'-'显示为方块的问题
#plt.rcParams['axes.unicode_minus'] = False 


os.chdir('/Users/seaswallow/Documents/try_better/pachong/')

plt.style.use('ggplot')   #默认绘图风格很难看，替换为好看的 ggplot 风格
fig = plt.figure(figsize=(8,5))   #设置图片大小
colors1 = '#6D6D6D'  #设置图表 title、text 标注的颜色
columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']  #设置表头
df = pd.read_csv('猫眼top100_1.csv',encoding = "gbk",header = None,names =columns,index_col = 'index')  #打开表格

# index_col = 'index' 将索引设为 index
df_score = df.sort_values('score',ascending = False)  #按得分降序排列
name1 = df_score.name[:10]      #x 轴坐标
score1 = df_score.score[:10]    #y 轴坐标  
plt.bar(range(10),score1,tick_label = name1)  #绘制条形图，用 range()能搞保持 x 轴正确顺序
plt.ylim ((9,9.8))  #设置纵坐标轴范围
plt.title('电影评分最高 top10',color = colors1) #标题
plt.xlabel('电影名称')      #x 轴标题
plt.ylabel('评分')          #y 轴标题

# 为每个条形图添加数值标签
for x,y in enumerate(list(score1)):
    plt.text(x,y+0.01,'%s' %round(y,1),ha = 'center',color = colors1)
pl.xticks(rotation=270)   #x 轴名称太长发生重叠，旋转为纵向显示
plt.tight_layout()    #自动控制空白边缘，以全部显示 x 轴名称
plt.rcParams['font.sans-serif'] = ['Simhei']

plt.rcParams['font.sans-serif']=['Simhei'] 
plt.rcParams['font.family']='sans-serif' 
# plt.savefig('电影评分最高 top10.png')   #保存图片
plt.show()

# 电影主要来自哪些国家
area_count = df.groupby(by = 'area').area.count().sort_values(ascending = False)
# 绘图方法 1
area_count.plot.bar(color = '#4652B1')  #设置为蓝紫色
pl.xticks(rotation=270)   #x 轴名称太长重叠，旋转为纵向
plt.title('各国/地区电影数量排名',color = colors1)
plt.xlabel('国家/地区')
plt.ylabel('数量(部)')
plt.show()

# 绘图方法 2
# plt.bar(range(11),area_count.values,tick_label = area_count.index)
area_count = df.groupby(by = 'area').area.count().sort_values(ascending = False)
area_count.plot.bar(color = '#4652B1')  #设置为蓝紫色
for x,y in enumerate(list(area_count.values)):
    plt.text(x,y+0.5,'%s' %round(y,1),ha = 'center',color = colors1)
plt.title('各国/地区电影数量排名',color = colors1)
plt.xlabel('国家/地区')
plt.ylabel('数量(部)')
plt.show()

## 从日期中提取年份
df['year'] = df['time'].map(lambda x:x.split('/')[0])
# print(df.info())
# print(df.head())
# 统计各年上映的电影数量
grouped_year = df.groupby('year')
grouped_year_amount = grouped_year.year.count()
top_year = grouped_year_amount.sort_values(ascending = False)
# 绘图
top_year.plot(kind = 'bar',color = 'orangered') #颜色设置为橙红色
for x,y in enumerate(list(top_year.values)):
    plt.text(x,y+0.1,'%s' %round(y,1),ha = 'center',color = colors1)
plt.title('电影数量年份排名',color = colors1)
plt.xlabel('年份(年)')
plt.ylabel('数量(部)')
plt.tight_layout()
# plt.savefig('电影数量年份排名.png')
plt.show()





