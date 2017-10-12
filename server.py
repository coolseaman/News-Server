#!/usr/bin/env python
# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import sys

# title = sys.argv[1]
# author = sys.argv[2]

def search(site, title, author):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    url = 'https://www.baidu.com/s?wd=site%3A' + site + '%20intitle%3A' + title + '%20' + author
    data = requests.get(url, headers=headers, verify=False).content
   
    soup = BeautifulSoup(data, 'html.parser')
    result = soup.find(id='1')

    return result

def main(title, author):
    result = []
    
    # 新浪新闻 sina.com.cn
    sina_result = search('news.sina.com.cn', title, author)
    if sina_result:
        sina_article_url = sina_result.h3.a['href']

        sina_article_content = requests.get(sina_article_url).content
        sina_soup_2 = BeautifulSoup(sina_article_content, 'html.parser', from_encoding='gb18030')
        
        try:
            sina_title = sina_soup_2.find(id='artibodyTitle').get_text()
            sina_pub_date = sina_soup_2.find(id='pub_date').get_text()
            if sina_soup_2.find(id='media_name'):
                sina_pub_media = sina_soup_2.find(id='media_name').get_text()
            else:
                sina_pub_media = sina_soup_2.find(class_='linkRed02').get_text()

            # print '新浪新闻', sina_title, sina_pub_date, sina_pub_media
            
            result.append({
                'site': '新浪新闻',
                'title': sina_title,
                'time': sina_pub_date,
                'source': sina_pub_media,
                'post_num': 0,
                'url': sina_article_url
            })
        except:
            print '【error】 页面格式无法解析'

    # 网易新闻 news.163.com
    net_result = search('news.163.com', title, author)
    if net_result:
        net_article_url = net_result.h3.a['href']

        net_article_content = requests.get(net_article_url).content
        net_soup_2 = BeautifulSoup(net_article_content, 'html.parser', from_encoding='gb18030')
        
        try:
            net_title = net_soup_2.find(id='epContentLeft').find('h1').get_text()
            net_pub_date = net_soup_2.find(class_='post_time_source').get_text().strip()[0:20]
            net_pub_media = net_soup_2.find(id='ne_article_source').get_text()
            net_post_num = net_soup_2.find(class_='post_cnum_tie').get_text()

            # print '网易新闻', net_title, net_pub_date, net_pub_media, net_post_num
            result.append({
                'site': '网易新闻',
                'title': net_title,
                'time': net_pub_date,
                'source': net_pub_media,
                'post_num': net_post_num,
                'url': net_article_url
            })
        except:
            print '【error】页面结构无法解析'
    
    # 搜狐新闻 news.sohu.com
    # sohu_url = 'https://www.baidu.com/s?wd=site%3Anews.sohu.com%20intitle%3A' + title + '%20' + author
    # sohu_data = search(sohu_url)
    # sohu_soup = BeautifulSoup(sohu_data, 'html.parser')
    # sohu_result = sohu_soup.find('1')

    return result
