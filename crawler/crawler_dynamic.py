# -*- coding: utf-8 -*-
import requests
import json, xlwt, os
# 应用宝爬虫
class crawlerDynamic():
    def getAppPageUrl(self, inputName):
        urlList = []
        urlString = ["", "MTA=", "MjA=", "MzA=", "NDA=", "NTA=", "NjA=", "NzA=", "ODA=", "OTA=", "MTAw=", "MTEw="]
        for urlS in urlString:
            url = 'http://sj.qq.com/myapp/searchAjax.htm?kw='+inputName+'&pns='+urlS+'&sid=0'
            urlList.append(url)
        return urlList

    def getAPPInfo(self, inputName):
        resultInfo = []
        urlList = self.getAppPageUrl(inputName)
        for url in urlList:
            cont = requests.get(url)
            print (url)
            content = cont.content
            conJson = json.loads(content, "utf-8")
            if conJson['success'] is True:
                appNum=len(conJson['obj']['appDetails'])
                for i in range(appNum):
                    result = {}
                    result['Name'] = conJson['obj']['appDetails'][i]['appName']
                    result['Size'] = conJson['obj']['appDetails'][i]['fileSize']/1024/1024
                    result['download-num'] = conJson['obj']['appDetails'][i]['appDownCount']
                    result['app-href'] = conJson['obj']['appDetails'][i]['apkUrl']
                    result['star-percent'] = conJson['obj']['appDetails'][i]['averageRating']
                    result['authorName'] = conJson['obj']['appDetails'][i]['authorName']
                    resultInfo.append(result)
            else:
                break
        return resultInfo

    def startCrawler(self, inputName):
        print ('Start crawling please wait...')
        appInfo = self.getAPPInfo(inputName)
        print (len(appInfo), 'apps have been crawled.')
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('sheet')
        sheet.write(0, 0, "APP_Name")
        sheet.write(0, 1, "APP_Size")
        sheet.write(0, 2, "APP_Download_num")
        sheet.write(0, 3, "APP_Star")
        sheet.write(0, 4, "APP_author")
        sheet.write(0, 5, "APP_url")
        for i in range(0, len(appInfo)):
            sheet.write(i + 1, 0, appInfo[i].get("Name"))
            sheet.write(i + 1, 1, appInfo[i].get("Size"))
            sheet.write(i + 1, 2, appInfo[i].get("download-num"))
            sheet.write(i + 1, 3, appInfo[i].get("star-percent"))
            sheet.write(i + 1, 4, appInfo[i].get("authorName"))
            sheet.write(i + 1, 5, appInfo[i].get("app-href"))
        currentPath = os.path.abspath('.')
        workbook.save(currentPath + '/crawl.xls')

crawler = crawlerDynamic()
crawler.startCrawler("直播")