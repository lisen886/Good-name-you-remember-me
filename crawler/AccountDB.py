# coding:utf-8
import xlrd,urllib,zipfile,os
from xlrd import open_workbook
from xlutils.copy import copy

accountDB = '/Users/****/Desktop/****.xls'
# 厂商so和名称以数据字典形式存储
dict = {'******.so': '**',
        '******.so': '**'}
data = xlrd.open_workbook(accountDB)
table = data.sheet_by_index(0)
rows = table.nrows
apks = table.col_values(5)

def downLoadAPK(row):
    so = []
    url = apks[row]
    print (url)
    temApkName = str(row) + ".apk"
    if url != '':
        try:
            urllib.urlretrieve(url, temApkName)
        except:
            print ("The %d URL requests timed out" % row)
            pass
    apkPath = os.getcwd() + "/"+temApkName
    if os.path.exists(apkPath):
        try:
            z = zipfile.ZipFile(apkPath, 'r')
            fnames = z.namelist()
            for i in fnames:
                if os.path.splitext(i)[1] == '.so':
                    sos = i.split("/")
                    so.append(sos[len(sos) - 1])
            return list(set(so))
        except:
            print ("The %d download file is not a zip file" % row)
            pass
def writeExcel(row):
    dictValue = []
    rexcel = open_workbook(accountDB)
    excel = copy(rexcel)
    table = excel.get_sheet(0)
    so = downLoadAPK(row)
    if so:
        lenso = len(so)
        for i in range(lenso):
            if dict.has_key(so[i]) is True:
                dictValue.append(dict.get(so[i]))
        table.write(row, 7, list(set(dictValue)))
        excel.save(accountDB)

# 通过给定APK的链接解析
def zipFile(file):
    fileList = []
    z = zipfile.ZipFile(file, 'r')
    fnames = z.namelist()
    for i in fnames:
        if os.path.splitext(i)[1] == '.so':
            sos = i.split("/")
            fileList.append(sos[len(sos) - 1])
    so = list(set(fileList))
    print (so)
    print ("========================")
    if so:
        lenso = len(so)
        for i in range(lenso):
            if dict.has_key(so[i]) is True:
                print (dict.get(so[i]))



def main():
    for i in range(1,rows):
        print (i)
        writeExcel(i)

if __name__=="__main__":
    main()
