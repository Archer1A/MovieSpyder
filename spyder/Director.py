#coding:utf-8
"""
author:Vic Wong
"""
import time

import requests
from bs4 import BeautifulSoup


def get_all_movie_messages():
    fo = open("result.txt","w+",encoding="utf-8") #打开一个文本 若不存在则自动创建
    for d in range(5):
        usl = "https://movie.douban.com/celebrity/1054398/movies?start=%d&format=pic&sortby=vote&"%(d*10)
        req =requests.get(url=usl) #取得网页
        print(req.text)
        soup = BeautifulSoup(req.text,"html.parser")#使用BeautifulSoup解析网页
        ul=soup.find_all("ul",_class="")

        for li in ul[3].find_all("li"):
            print("*"*20)
            url=li.find("h6").a.get("href")
            list=li.find("h6").get_text().split("\n")
            movie_name = list[1].strip()
            print(movie_name)
            year = list[2].strip()
            print(year)
            role = list[3].strip()
            print(role)
            fo.write(movie_name+"\t"+url+"\t"+year+"\t"+role+"\t"+"\n")
        time.sleep(3)
get_all_movie_messages()