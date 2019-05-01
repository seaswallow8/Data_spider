#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 21:31:23 2019

@author: seaswallow
"""

import requests
from requests.exceptions import RequestException
import re
from bs4 import BeautifulSoup
import time
import os 
import csv
os.chdir('/Users/seaswallow/Documents/try_better/pachong/')


#https://movie.douban.com/subject/26100958/comments?start=0&limit=20&sort=new_score&status=P
#https://movie.douban.com/subject/26100958/comments?start=20&limit=20&sort=new_score&status=P
#https://movie.douban.com/subject/26100958/comments?start=40&limit=20&sort=new_score&status=P



### 抓取网页源码
url = 'https://movie.douban.com/subject/26100958/comments?start=0&limit=20&sort=new_score&status=P'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
### 不加headers爬不了
response = requests.get(url, headers=headers)
html=response.text

from lxml import etree
parse = etree.HTML(html)

#//*[@id="comments"]/div[1]/div[1]/a
#//*[@id="comments"]/div[2]/div[1]/a
#//*[@id="comments"]/div[3]/div[1]/a

items = parse.xpath('//*[@id="comments"]/div/div[1]')
for item in items:
    #用户名
    name=item.xpath('./a/@title')[0]
    print('name'+name)


#//*[@id="comments"]/div[16]/div[2]/h3/span[2]/span[2]
#//*[@id="comments"]/div[15]/div[2]/h3/span[2]/span[3]
#//*[@id="comments"]/div[1]/div[2]/h3/span[2]/span[3]  
    
## 模拟豆瓣登陆
class DouBanLogin(object):
    def __init__(self, account, password):
        self.url = "https://accounts.douban.com/j/mobile/login/basic"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        """初始化数据"""
        self.data = {
            "ck": "",
            "name": account,
            "password": password,
            "remember": "true",
            "ticket": ""
        }
        self.session = requests.Session()

    def get_cookie(self):
        """模拟登陆获取cookie"""
        html = self.session.post(
            url=self.url,
            headers=self.headers,
            data=self.data
        ).json()
        if html["status"] == "success":
            print("恭喜你，登陆成功")

    def get_user_data(self):
        """获取用户数据表明登陆成功"""
        # TODO: 这里填写你用户主页的url
        url = "https://www.douban.com/people/185659618/"
        # 获取用户信息页面
        html = self.session.get(url).text
        print(html)
        return html

    def run(self):
        """运行程序"""
        self.get_cookie()
        self.get_user_data()
   
    
    
        
def fulian4(html):
    parse = etree.HTML(html)
    items = parse.xpath('//*[@id="comments"]/div/div[2]')
    for item in items:
        yield{
             #'date': item.xpath('.//span[3]/@title')[0],
             'short': item.xpath('./p/span/text()')[0]
        }  
##### 将获取的信息的字典以csv表单存储起来

def write_to_file(item):
    with open('复联短评.csv', 'a', encoding='utf_8_sig',newline='') as f:
        # 'a'为追加模式（添加）
        # utf_8_sig格式导出csv不乱码 
        fieldnames = ['date', 'short']
        w = csv.DictWriter(f,fieldnames = fieldnames)
        # w.writeheader()
        w.writerow(item)

def main(offset):
    ## 获取html文本
    url = 'https://movie.douban.com/subject/26100958/comments?start='+str(offset)+'&limit=20&sort=new_score&status=P'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    ### 不加headers爬不了
    response = requests.get(url, headers=headers)
    html= response.text
    # print(html)
    # parse_one_page2(html)
    for item in fulian4(html):  # 切换内容提取方法
        print(item)
        write_to_file(item)
        #download_thumb(item['name'], item['thumb'],item['index'])

     
if __name__ == '__main__':
    ## 模拟登陆
    login = DouBanLogin('13511096286','987620haiyan')
    login.run()
    for i in range(11):
         main(i * 20)
         print('第'+str(i)+'页！')
         time.sleep(0.5)













#//*[@id="comments"]/div[1]/div[2]/p/span/text()
#//*[@id="comments"]/div[2]/div[2]/p/span
#//*[@id="comments"]/div[1]/div[2]/p/span/text()    
#//*[@id="comments"]/div[3]/div[2]/p/span/text()
#//*[@id="comments"]/div[6]/div[2]/p/span/text()
items = parse.xpath('//*[@id="comments"]/div/div[2]')
for item in items:
    short=item.xpath('./p/span/text()')[0]
    print('short'+short)