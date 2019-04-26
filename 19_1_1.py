#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:45:07 2019

@author: seaswallow
"""

import requests
from requests.exceptions import RequestException
import re
from bs4 import BeautifulSoup
import time
import os 
os.chdir('/Users/seaswallow/Documents/try_better/pachong/')

def get_release_time(data):
    pattern = re.compile(r'(.*?)(\(|$)')
    items = re.search(pattern, data)
    if items is None:
        return '未知'
    return items.group(1)  # 返回匹配到的第一个括号(.*?)中结果即时间


# 提取国家/地区函数
def get_release_area(data):
    pattern = re.compile(r'.*\((.*)\)')
    # $表示匹配一行字符串的结尾，这里就是(.*?)；\(|$,表示匹配字符串含有(,或者只有(.*?)
    items = re.search(pattern, data)
    if items is None:
        return '未知'
    return items.group(1)

## 爬取所需要的信息
def parse_one_page4(html):
    soup = BeautifulSoup(html,'lxml')
    items = range(10)
    for item in items:
        yield{

            'index': soup.find_all(class_='board-index')[item].string,
            'thumb': soup.find_all(class_ = 'board-img')[item].attrs['data-src'],
            # 用.get('data-src')获取图片src链接，或者用attrs['data-src']
            'name': soup.find_all(name = 'p',attrs = {'class' : 'name'})[item].string,
            'star': soup.find_all(name = 'p',attrs = {'class':'star'})[item].string.strip()[3:],
            'time': get_release_time(soup.find_all(class_ ='releasetime')[item].string.strip()[5:]),
            'area': get_release_area(soup.find_all(class_ ='releasetime')[item].string.strip()[5:]),
            'score':soup.find_all(name = 'i',attrs = {'class':'integer'})[item].string.strip() + soup.find_all(name = 'i',attrs = {'class':'fraction'})[item].string.strip()
        }

## 1.给定网页爬html信息的函数
def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        # 不加headers爬不了
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None

## 2. 从html中抓取自己需要的信息      
def main(offset):
    url = 'http://maoyan.com/board/4?offset='+ str(offset)
    html = get_one_page(url)
    
    for item in parse_one_page4(html):  
        print(item)


if __name__ == '__main__':
    for i in range(10):
         main(i * 10)
         time.sleep(0.5)
         
         
         
##### 将获取的信息的字典以csv表单存储起来
import csv
def write_to_file3(item):
    with open('猫眼top100.csv', 'a', encoding='utf_8_sig',newline='') as f:
        # 'a'为追加模式（添加）
        # utf_8_sig格式导出csv不乱码 
        fieldnames = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
        w = csv.DictWriter(f,fieldnames = fieldnames)
        # w.writeheader()
        w.writerow(item)


### 储存封面图片
def download_thumb(name, url,num):
    try:
        response = requests.get(url)
        with open('封面图/' + name + '.jpg', 'wb') as f:
            f.write(response.content)
            print('第%s部电影封面下载完毕' %num)
            print('------')
    except RequestException as e:
        print(e)
        pass


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    # parse_one_page2(html)

    for item in parse_one_page4(html):  # 切换内容提取方法
        print(item)
        write_to_file3(item)
        #download_thumb(item['name'], item['thumb'],item['index'])

if __name__ == '__main__':
      for i in range(10):
         main(i * 10)
         time.sleep(0.5)
