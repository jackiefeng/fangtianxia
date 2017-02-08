#!/usr/bin/env python
#coding:utf-8

import re
import time
import urllib
import requests

filePath = 'fangtianxia_result.txt'


def writeFile(path, line):
    fd = open(path, 'a+')
    fd.write(line)
    fd.close()

def writeFiles(path, lines):
    fd = open(path, 'a+')
    fd.writelines(lines)
    fd.close()


def readHtml(recordList):
    url = 'http://esf.ts.fang.com/house/h316/'
    r = requests.get(url=url)
    html = r.text.encode('utf-8')
    reg = r'a href="(.*)"  target="_blank"'
    re_ = re.compile(reg, re.M)
    list_ = re.findall(re_, html)
    for key in list_:
        #如果已有记录，则忽略
        if key in recordList:
            continue

        recordList.append(key)

        url = 'http://esf.ts.fang.com' + key
        r = requests.get(url=url)
        html = r.text.encode('utf-8')

        #标题
        postTitle = html.find('<div class="title">')
        html = html[postTitle:]
        postTitleBegin = html.find('<h1>')
        postTitleEnd = html.find('</h1>')
        title = html[postTitleBegin+4:postTitleEnd].strip()
        html = html[postTitleEnd+4:]

        #发布日期
        postDateBegin = html.find('发布时间')
        postDateEnd = html.find('</p>')
        date = html[postDateBegin+15:postDateEnd].strip()
        html = html[postDateEnd:]

        postBegin = html.find('<dl>')
        postEnd = html.find('</dl>')
        line = html[postBegin+4:postEnd]
        html = html[postEnd+5:]

        #总价
        postMoneyBegin = line.find('class="red20b">')
        postMoneyEnd = line.find('</span>', postMoneyBegin)
        money = line[postMoneyBegin+15:postMoneyEnd]
        line = line[postMoneyEnd+12:].strip()

        #均价
        postAvgBegin = line.find('(')
        postAvgEnd = line.find('元/')
        avg = line[postAvgBegin+1:postAvgEnd]
        line = line[postAvgEnd:]

        #户型
        postHotelBegin = line.find('型')
        postHotelBegin = line.find('>', postHotelBegin)
        postHotelEnd = line.find('</dd>')
        hotel = line[postHotelBegin+1:postHotelEnd]
        line = line[postHotelEnd:]

        #面积
        postAreaBegin = line.find('"black ">')
        postAreaEnd = line.find('</span>')
        area = line[postAreaBegin+9:postAreaEnd-3]
        line = line[postAreaEnd:]

        postBegin = html.find('<dl>')
        postEnd = html.find('</dl>')
        line = html[postBegin+5:postEnd]

        #年代
        postYearBegin = line.find('代：</span>')
        postYearEnd = line.find('</dd>', postYearBegin)
        year = line[postYearBegin+13:postYearEnd]
        line = line[postYearEnd+5:]

        #方向
        postDirectionBegin = line.find('向：</span>')
        postDirectionEnd = line.find('</dd>', postDirectionBegin)
        direction = line[postDirectionBegin+13:postDirectionEnd]
        line = line[postDirectionEnd+5:]

        #楼层
        postFloorBegin = line.find('层：</span>')
        postFloorEnd = line.find('</dd>', postFloorBegin)
        floor = line[postFloorBegin+13:postFloorEnd]
        line = line[postFloorEnd+5:]

        #装修
        postRedesignBegin = line.find('修：</span>')
        postRedesignEnd = line.find('</dd>', postRedesignBegin)
        redesign = line[postRedesignBegin+13:postRedesignEnd]
        line = line[postRedesignEnd+5:]

        #小区
        postVillageBegin = line.find('class="blue">')
        postVillageEnd = line.find('</a>', postVillageBegin)
        village = line[postVillageBegin+13:postVillageEnd]
        line = line[postVillageEnd+5:]

        #小区均价
        postVillageAvgBegin = html.find('"red20b">')
        postVillageAvgEnd= html.find('</span>', postVillageAvgBegin)
        villageAvg = html[postVillageAvgBegin+9:postVillageAvgEnd]

        #下载图片
        #TODO

        #通知
        #TODO

        #写入到文件
        #网址,发布日期,总价,均价,小区均价,小区,面积,楼层,户型,年代,方向,装修
        line = '%s,%s,总价(%s),均价(%s),小区均价(%s),%s,面积(%s),%s,%s,%s,%s,%s\r\n' % (key, date, money, avg, villageAvg, village, area, floor, hotel, year, direction, redesign)
        writeFile(filePath, line)
        print line.decode('utf-8')
        #break

if __name__ == '__main__':
    recordList = []

    #读取文件
    #TODO
    while True:
        readHtml(recordList)
        time.sleep(10)










