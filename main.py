#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import bs4
import time
import random
from pymongo import MongoClient

class Lianjia():
    def __init__(self):
        pass


    def getContents(self,url):

        headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'hz.lianjia.com',
        'Referer':'https://hz.lianjia.com/xiaoqu/',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36'
        }

        resp = requests.get(url,headers=headers)
        cookies = resp.cookies
        contents = resp.content
        soup = bs4.BeautifulSoup(contents, 'html.parser')

        return contents


    def save(self,fileName,contents):
        with open(fileName,'wb+') as file:
            file.writelines(contents)
            file.close()
        return(True)

    def read(self,filePath):
        with open(filePath) as file:
            contents = file.readlines()
            file.close()
            return ''.join(contents)



    def xiaoquListParser(self,url,contents=None):
        if contents == None:
            contents = self.getContents(url)
        else:
            contents = contents
        soup = bs4.BeautifulSoup(contents)
        xiaoquList = soup.find_all(class_='clear xiaoquListItem')
        items = []
        for xiaoqu in xiaoquList:

            #获取小区url 和小区名称
            item =xiaoqu.find(class_='title')
            link = item.a['href']
            name = item.a.string

            #获取小区成交数据url
            selled = xiaoqu.find(class_='houseInfo').a['href']

            #获取小区均价
            price = xiaoqu.find(class_='totalPrice').span.string
            try:
                price = int(price)
            except:
                print '无数据'
                price    = 0

            #获取小区挂牌数量
            count = xiaoqu.find(class_='totalSellCount').span.string
            try:
                count = int(count)
            except:
                print '无挂牌'
                count = 0


            print  name ,price,count,link ,selled
            ditile = {'link':link,'name':name,'price':price,'count':count,'selledUrl':selled}
            items.append(ditile)
        return items

    def xiaoquInfoParser(self,url):
        contents = self.getContents(url)
        soup = bs4.BeautifulSoup(contents)
        infos = soup.find_all('span',class_='xiaoquInfoContent')
        l = []
        for info in infos:
            i = info.string
            l.append(i)
        return l


    def pageParser(self,url,contents=None):
        if contents ==None:
            contents = self.getContents(url)
        else:
            contents = contents
        soup = bs4.BeautifulSoup(contents)
        pages = soup.find('div', class_='page-box house-lst-page-box')
        d = eval(pages['page-data'])
        page = d['totalPage']
        return page

    def selledParser(self,url):
        pass


def delay(a,b):
    t = random.randint(a,b)
    print '休眠%d秒'%t
    time.sleep(t)





# for i in range(1,9):
#     url = 'https://hz.lianjia.com/xiaoqu/binjiang/'+'pg'+str(i)
#     fileName = str(i)+'.html'
#     parser(url,fileName=fileName)
#     t = random.randint(10,60)
#     print '休眠%d秒'%t
#     time.sleep(t)
#     print '完成第%d爬取'%i
#     i +=1


if __name__=='__main__':
    baseurl = 'https://hz.lianjia.com/xiaoqu/'
    areas = ['xihu','xiacheng','jianggan','gongshu','shangcheng','binjiang','yuhang','xiaoshan','xiasha']
    befor = time.time()
    #数据库实例化
    client = MongoClient('localhost',27017)
    db = client['lj']

    lianjia = Lianjia()

    for area in areas:
        print '正在爬取%s'%area
        coll = db['infos']
        url = baseurl+area
        page = lianjia.pageParser(url)
        print '共%d页'%page
        for i in range(1, page+1):
            pageUrl = url+ '/pg'+str(i)
            #contents = lianjia.getContents(pageUrl)
            # print type(contents)
            # print contents
            print '解析第%d页' % i
            datas = lianjia.xiaoquListParser(pageUrl)
            print '正在存储'
            coll.insert(datas)
            delay(10,40)

    print '解析完成'
    print  '用时%f分钟'%((time.time()-befor)/60)

        # for data in datas:
        #     k = ['nd', 'jg', 'wyf', 'wygs', 'kfs', 'ds', 'hs', 'qt']
        #
        #     #############获取小区基本你信息#############
        #     url = data['link']
        #     items = lianjia.xiaoquInfoParser(url)#获取小区基本星系
        #     d = dict(zip(k,items))
        #     data = dict(data,**d)
        #     t = random.randint(10,60)
        #     print '休眠%d秒'%t
        #     time.sleep(t)
        #     #############获取小区基本你信息#############




