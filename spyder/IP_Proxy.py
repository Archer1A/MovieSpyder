#coding:utf-8
#author:wangyijun
import requests
import time
from bs4 import BeautifulSoup
import pymongo
from queue import Queue
#连接Mongodb数据库
db=pymongo.MongoClient("127.0.0.1",27017)
#指定将要写入Mongodb的表
colletion=db["IPproxy"]["IPproxy"]
headers = {
'Cookie':'ASPSESSIONIDASSCTBAA=AICDINOABHBCCCIBPEDDIOML; UM_distinctid=160b1e97b5b153-036f40195762bf-5a442916-100200-160b1e97b5d200; CNZZDATA1253438097=2012153161-1514811618-null%7C1514811618',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}
for i in range(10):
    #爬取http://www.nianshao.me/前10页的所有代理ip
    req = requests.get("http://www.nianshao.me/?page=%s"%(str(i)),headers=headers)
    #使用BeautifulSoup解析网页
    soup = BeautifulSoup(req.content.decode("gbk"),"html.parser")
    for i in soup.find_all("table")[0].find_all("tr")[1:]:
        #获得ip和端口
        ip=i.find_all("td")[0].get_text()
        port=i.find_all("td")[1].get_text()
        proxies={
            "http":"http://"+ip+":"+port
        }
        print("正在测试地址："+ip+":"+port)
        try:
            #测试该代理ip是否有效；http://icanhazip.com/ 该网站返回访问者ip
            test=requests.get("http://icanhazip.com/",proxies=proxies,timeout=5)
            if(test.status_code==200):
                print(test.text.strip()+"有效")
                #写入数据库中
                colletion.insert({"ip":"http://"+ip+":"+port})
            else:
                print(ip+"无效......")
        except:
            print(ip + "无效......")