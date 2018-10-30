# -*- coding:utf-8 -*-
import urllib2, re, os, xlwt
from bs4 import BeautifulSoup
import requests
class AppSipder:
    # 百度手机助手
    def __init__(self, inputName, pageNum):
        self.categoryPageURL_list = []
        for x in range(0, pageNum):
            # self.URL = 'http://shouji.baidu.com/s?data_type=app&multi=0&ajax=1&wd=' + inputName + \
            #            '&page=' + str(x) + '&_=1509289652244'
            self.URL = 'http://shouji.baidu.com/s?data_type=app&multi=0&ajax=1&wd=' + inputName + \
                            '&page='+str(x)
            self.categoryPageURL_list.append(self.URL)

    def getAppDetailPageURL(self):
        categoryPageURL_list = self.categoryPageURL_list
        appDetailPageURL_list = []
        for url in categoryPageURL_list:
            print (url)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read().decode("unicode-escape")
            pattern = re.compile('<div.*?app">.*?<a target="_blank" href="(.*?)".*?>', re.S)
            resultStr = re.findall(pattern, content)
            for result in resultStr:
                appDetailPageURL = 'http://shouji.baidu.com' + result
                appDetailPageURL_list.append(appDetailPageURL)
        return appDetailPageURL_list

    def getAppInfo(self, appURL):
        print (appURL)
        try:
            request = urllib2.Request(appURL)
            response = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print ("Get appInfo failed:", e.reason)
            return None
        content = response.read().decode("utf-8")
        result = {}
        # 得到app名字
        pattern = re.compile('<span>(.*?)</span>')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['Name'] = resultStr.group(1)

        # 得到app大小，需要对字符串处理
        pattern = re.compile('<span class="size">(.*?)</span>')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['Size'] = (((resultStr.group(1)).split(':'))[1]).strip()

        # 下载量
        pattern = re.compile('<span class="download-num">(.*?)</span>')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['download-num'] = (((resultStr.group(1)).split(':'))[1]).strip()

        # 下载地址
        pattern = re.compile('<div.*?area-download">.*?<a target="_blank.*?href="(.*?)".*?>', re.S)
        resultStr = re.search(pattern, content)
        if resultStr:
            result['app-href'] = resultStr.group(1)

        # 评论次数
        pattern = re.compile('<span class="star-percent" style="width:(.*?)">')
        resultStr = re.search(pattern, content)
        if resultStr:
            result['star-percent'] = resultStr.group(1)
        print (result)
        return result

    def startSpider(self):
        print ('Start crawling please wait...')
        appDetailPageURL_list = self.getAppDetailPageURL()
        resultInfo = []
        for url in appDetailPageURL_list:
            try:
                resultInfo.append(self.getAppInfo(url))
            except:
                print ("这个网址有毒：%s" % url)
        print (len(resultInfo), 'apps have been crawled.')
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('sheet')
        sheet.write(0, 0, "APP_Name")
        sheet.write(0, 1, "APP_Size")
        sheet.write(0, 2, "APP_Download_num")
        sheet.write(0, 3, "APP_Star")
        sheet.write(0, 4, "APP_author")
        sheet.write(0, 5, "APP_url")
        for i in range(0, len(resultInfo)):
            sheet.write(i+1, 0, resultInfo[i].get("Name"))
            sheet.write(i+1, 1, resultInfo[i].get("Size"))
            sheet.write(i+1, 2, resultInfo[i].get("download-num"))
            sheet.write(i+1, 3, resultInfo[i].get("star-percent"))
            sheet.write(i+1, 5, resultInfo[i].get("app-href"))
        currentPath = os.path.abspath('.')
        workbook.save(currentPath + '/crawl.xls')

Spider = AppSipder("直播", 13)
Spider.startSpider()