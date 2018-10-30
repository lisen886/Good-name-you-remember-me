# coding:utf-8
import xlrd,xlwt, os, requests
from bs4 import BeautifulSoup
from xlrd import open_workbook
from xlutils.copy import copy
# ASO100爬虫
currentPath = os.path.abspath('.')
accountDB = currentPath + '/crawl.xls'
data = xlrd.open_workbook(accountDB)
table = data.sheet_by_index(0)
rows = table.nrows
# appName的列数（index）
apksNameList = table.col_values(0)
def getAuthorNameByASO100(inputName):
    authorName = []
    url = 'https://aso100.com/search/android?country=cn&search='+inputName
    print (url)
    r = requests.get(url)
    t = r.text
    x = BeautifulSoup(t, "html.parser")
    divtaglist = x.find_all('div', attrs={'class': 'media'})
    for i in range(0, len(divtaglist)):
        h4tag = divtaglist[i].find('h4', attrs={'class': 'media-heading'})
        atag = h4tag.find('a')
        appName = atag.text.encode("utf-8").split("、")[1]
        if appName == inputName.encode("utf-8"):
            nameTag = divtaglist[i].find('div', attrs={'class': 'media-auther'})
            print (nameTag.text.encode("utf-8"))
            authorName.append(nameTag.text)
    return list(set(authorName))

def getAuthorNameList():
    authorNameList = []
    for i in range(1, len(apksNameList)):
        authorName = getAuthorNameByASO100(apksNameList[i])
        authorNameList.append(authorName)
    return authorNameList

def startCrawlAuthorName():
    rexcel = open_workbook(accountDB)
    excel = copy(rexcel)
    table = excel.get_sheet(0)
    authorList = getAuthorNameList()
    for i in range(0, len(authorList)):
        table.write(i + 1, 4, authorList[i])
    excel.save(accountDB)

startCrawlAuthorName()