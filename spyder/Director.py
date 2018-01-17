#coding:utf-8
"""
author:Vic Wong
"""
import time
import threading
import requests
from bs4 import BeautifulSoup

k=0
lock=threading.Lock()
fo = open("result.txt","a",encoding="utf-8") #打开一个文本 若不存在则自动创建
def get_all_movie_messages():
    global k
    global lock
    while k <6:
        lock.acquire()
        url = "https://movie.douban.com/celebrity/1054398/movies?start=%s&format=pic&sortby=vote&"%(k*10)
        k+=1
        print(k)
        lock.release()
        req =requests.get(url=url) #取得网页
        print("线程%s正在爬取%s"%(threading.current_thread().getName(),url))
       # print(k)
        soup = BeautifulSoup(req.text,"html.parser")#使用BeautifulSoup解析网页
        ul=soup.find_all("ul",_class="")#通过BeautifulSoup找到所有的ul标签

        for li in ul[3].find_all("li"):#在ul标签中找到所以的li标签
            #print("*"*20)
            url=li.find("h6").a.get("href")#获取超链接
            list=li.find("h6").get_text().split("\n")#获取标签中的文本
            movie_name = list[1].strip()
            #print(movie_name)
            year = list[2].strip()
            #print(year)
            role = list[3].strip()
            #print(role)
            fo.write(movie_name+"\t"+url+"\t"+year+"\t"+role+"\t"+"\n")
        time.sleep(3)
thread_1=threading.Thread(target=get_all_movie_messages)
thread_2=threading.Thread(target=get_all_movie_messages)
thread_3=threading.Thread(target=get_all_movie_messages)
thread_1.setDaemon(False)
thread_2.setDaemon(False)
thread_1.start()
thread_3.start()
thread_2.start()
thread_1.join()
thread_2.join()
thread_3.join()
fo.close()