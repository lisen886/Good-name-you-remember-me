#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import os,re,sys,platform,json
if sys.version < "3":
    import urllib2
else:
    # 因为打包程序没法使用urllib，改用urllib2
    from urllib import request
def execInstallCMD(pwd):
    cmd = "start /wait "+pwd+" /S"
    f = os.system(cmd)
    if str(f) != "0":
        return False

def execUninstallFirefoxCMD():
    askStatus = tkinter.messagebox.askyesno('提示', '是否卸载浏览器')
    if askStatus == True:
        cmd = r'"C:\Program Files\Mozilla Firefox\uninstall\helper.exe" /S'
        f = os.system(cmd)
        if str(f) != "0":
            return False
    else:
        return "cancle"

def execUninstallChromeCMD():
    askStatus = tkinter.messagebox.askyesno('提示', '是否卸载浏览器')
    if askStatus == True:
        os.system("taskkill /F /IM chrome.exe /T")
        get_version_cmd = r'wmic datafile where name="C:\\Users\\%Username%\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe" get Version /value'
        f = os.popen(get_version_cmd)
        out = f.read()
        f.close()
        chrome_version = out.split("=")[-1].strip()
        uninstallchrome_cmd = "C:\\Users\\%Username%\\AppData\\Local\\Google\\Chrome\\Application\\" + str(chrome_version) + "\\Installer\\setup.exe --uninstall --multi-install --chrome"
        f = os.system(uninstallchrome_cmd)
        if str(f) != "0" and str(f) != "19":
            return False
    else:
        return "cancle"
# *********************** macOS ***********************#
detachDiskTempList = []
def execInstallCMD_MACOS(pwd,Btype):
    attachCMD = "hdiutil attach " + pwd
    out = os.system(attachCMD)
    # f = os.popen(attachCMD)
    # out = f.read()
    # f.close()
    askStatus = tkinter.messagebox.askyesno('提示', '是否卸载自己的浏览器重新安装')
    if askStatus == True:
        if Btype == "Chrome":
            os.system("rm -rf /Applications/Google\ Chrome.app/")
            os.system("cp -r /Volumes/Google\ Chrome/Google\ Chrome.app/ /Applications/Google\ Chrome.app/")
        elif Btype == "Firefox":
            os.system("rm -rf /Applications/Firefox/")
            os.system("cp -r /Volumes/Firefox/Firefox.app/ /Applications/Firefox.app/")
        else:
            print("...")
    else:
        if Btype == "Chrome":
            os.system("rm -rf /Applications/Google\ ChromeTemp.app/")
            os.system("cp -r /Volumes/Google\ Chrome/Google\ Chrome.app/ /Applications/Google\ ChromeTemp.app/")
        elif Btype == "Firefox":
            os.system("rm -rf /Applications/FirefoxTemp.app/")
            os.system("cp -r /Volumes/Firefox/Firefox.app/ /Applications/FirefoxTemp.app/")
        else:
            print("...")
    if Btype == "Chrome":
        os.system("hdiutil detach /Volumes/Google\ Chrome/")
    else:
        os.system("hdiutil detach /Volumes/Firefox/")
    # detachDiskList = out.split("\t\n")
    # for detachDiskI in detachDiskList:
    #     if "/Volumes/" in detachDiskI:
    #         detachDisk = detachDiskI.split("\t")[0].strip()
    #         detachCMD = "hdiutil detach " + detachDisk
    #         os.system(detachCMD)
def execOpenBrowser_MACOS(pwd,Btype):
    attachCMD = "hdiutil attach " + pwd
    f = os.popen(attachCMD)
    out = f.read()
    f.close()
    detachDiskList = out.split("\t\n")
    for detachDiskI in detachDiskList:
        if "/Volumes/" in detachDiskI:
            detachDisk = detachDiskI.split("\t")[0].strip()
            detachDiskTempList.append(detachDisk)
    if Btype == "Chrome":
        os.system("open /Volumes/Google\ Chrome/Google\ Chrome.app/")
    elif Btype == "Firefox":
        os.system("open /Volumes/Firefox/Firefox.app/")
    else:
        print("...")
def execCloseBrowser_MACOS(Btype):
    if Btype == "Chrome":
        os.system("ps -ef | grep Google | grep -v grep | awk '{print $2}' | xargs kill -9")
    elif Btype == "Firefox":
        os.system("ps -ef | grep Firefox | grep -v grep | awk '{print $2}' | xargs kill -9")
    detachDisk = detachDiskTempList[0]
    detachCMD = "hdiutil detach "+detachDisk
    os.system(detachCMD)
    detachDiskTempList.clear()
def execUninstallChromeCMD_MACOS():
    askStatus = tkinter.messagebox.askyesno('提示', '是否卸载浏览器')
    if askStatus == True:
        f = os.system("rm -rf /Applications/Google\ Chrome.app")
        if str(f) != "0":
            return False
    else:
        return "cancle"
def execUninstallFirefoxCMD__MACOS():
    askStatus = tkinter.messagebox.askyesno('提示', '是否卸载浏览器')
    if askStatus == True:
        f = os.system("rm -rf /Applications/Firefox.app/")
        if str(f) != "0":
            return False
    else:
        return "cancle"
# **********************************************#
def downloadPackage(url):
    # http://10.80.0.160:8888/Firefox60.0.exe
    packageName = url.split("/")[-1]
    if platform.system() == "Windows":
        packagePWD = os.getcwd() + "\\" + packageName
    else:
        packagePWD = "/tmp/" + packageName
        # packagePWD = os.getcwd() + "/" + packageName
    if sys.version < "3":
        f = urllib2.urlopen(url)
        data = f.read()
        with open(packageName, "wb") as code:
            code.write(data)
    else:
        if platform.system() == "Windows":
            request.urlretrieve(url, "./%s" % packageName)
        else:
            request.urlretrieve(url,"%s"%packagePWD)
    return packagePWD
def getJsonData(browserType,version):
    try:
        if platform.system() == "Windows":
            with open("./browserConfig.json","r") as load_f:
                load_dict = json.load(load_f)
                appPWD = os.getcwd()
                versionPWD = appPWD+load_dict[browserType][str(version)].replace("/", "\\")
                return load_dict[browserType],versionPWD
        else:
            # mac 打包后os.getcwd() 不可用，，，改成了这种S13的操作
            appPWD = os.path.abspath(sys.argv[0]).split("installApplication.app")[0]
            jsonPWD = appPWD+"/browserConfig.json"
            with open(jsonPWD,"r") as load_f:
                load_dict = json.load(load_f)
                versionPWD = appPWD+load_dict[browserType][str(version)]
                return load_dict[browserType],versionPWD
    except:
        tkinter.messagebox.showwarning('警告', '请将browserConfig.json移到程序相同路径下或者json文件格式有问题')
def clickMeInstallChrome():  # 当acction被点击时,该函数则生效
    if sendChromeAddress.get() != "":
        if re.match("http",sendChromeAddress.get()):
            packagePWD = downloadPackage(sendChromeAddress.get())
            try:
                if platform.system() == "Windows":
                    state = execInstallCMD(packagePWD)
                else:
                    state = execInstallCMD_MACOS(packagePWD,"Chrome")
                if state == False:
                    tkinter.messagebox.showerror('错误', '安装失败')
                    # installChromeAction.configure(text='Install fail ')
                else:
                    tkinter.messagebox.showinfo('提示', '安装成功')
            except:
                tkinter.messagebox.showerror('错误', '安装失败')
                # installChromeAction.configure(text='Install fail ')
            if platform.system() == "Windows":
                os.system("del %s" % packagePWD)
            else:
                os.system("rm -f %s" % packagePWD)
        else:
            try:
                if platform.system() == "Windows":
                    state = execInstallCMD(sendChromeAddress.get())
                else:
                    state = execInstallCMD_MACOS(sendChromeAddress.get(),"Chrome")
                if state == False:
                    tkinter.messagebox.showerror('错误', '安装失败')
                    # installChromeAction.configure(text='Install fail ')
                else:
                    tkinter.messagebox.showinfo('提示', '安装成功')
                    # installChromeAction.configure(text='Install successed ')  # 设置button显示的内容
                    # installChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
            except:
                tkinter.messagebox.showerror('错误', '安装失败')
                # installChromeAction.configure(text='Install fail ')
    else:
        versionPWD = ""
        if platform.system() == "Windows":
            winChromeDict, winChromeVerionPWD = getJsonData("winchromeList", ChromeVersionList.get())
            if ChromeVersionList.get() in winChromeDict:
                versionPWD = winChromeVerionPWD
            else:
                tkinter.messagebox.showwarning('警告', '程序字典中缺失该版本的键值')
        else:
            macChromeDict,macChromeVerionPWD = getJsonData("macchromeList",ChromeVersionList.get())
            if ChromeVersionList.get() in macChromeDict:
                versionPWD = macChromeVerionPWD
            else:
                tkinter.messagebox.showwarning('警告', '程序字典中缺失该版本的键值')
        if os.path.exists(versionPWD):
            try:
                if platform.system() == "Windows":
                    state = execInstallCMD(versionPWD)
                else:
                    state = execInstallCMD_MACOS(versionPWD,"Chrome")
                if state == False:
                    tkinter.messagebox.showerror('错误', '安装失败')
                else:
                    tkinter.messagebox.showinfo('提示', '安装成功')
            except:
                tkinter.messagebox.showerror('错误', '安装失败')
        else:
            tkinter.messagebox.showwarning('警告', '这个版本的安装包不存在')

def clickMeInstallFirefox():
    if sendFirefoxAddress.get() != "":
        if re.match("http",sendFirefoxAddress.get()):
            packagePWD = downloadPackage(sendFirefoxAddress.get())
            try:
                if platform.system() == "Windows":
                    state = execInstallCMD(packagePWD)
                else:
                    state = execInstallCMD_MACOS(packagePWD,"Firefox")
                if state == False:
                    tkinter.messagebox.showerror('错误', '安装失败')
                    # installFirefoxAction.configure(text='Install fail ')
                else:
                    tkinter.messagebox.showinfo('提示', '安装成功')
                    # installFirefoxAction.configure(text='Install successed ')  # 设置button显示的内容
                    # installFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
            except:
                # installFirefoxAction.configure(text='Install fail ')
                tkinter.messagebox.showerror('错误', '安装失败')
            if platform.system() == "Windows":
                os.system("del %s" % packagePWD)
            else:
                os.system("rm -f %s" % packagePWD)
        else:
            try:
                if platform.system() == "Windows":
                    state = execInstallCMD(sendFirefoxAddress.get())
                else:
                    state = execInstallCMD_MACOS(sendFirefoxAddress.get(),"Firefox")
                if state == False:
                    # installFirefoxAction.configure(text='Install fail ')
                    tkinter.messagebox.showerror('错误', '安装失败')
                else:
                    # installFirefoxAction.configure(text='Install successed ')  # 设置button显示的内容
                    # installFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
                    tkinter.messagebox.showinfo('提示', '安装成功')
            except:
                # installFirefoxAction.configure(text='Install fail ')
                tkinter.messagebox.showerror('错误', '安装失败')
    else:
        versionPWD = ""
        if platform.system() == "Windows":
            winFirefoxDict, winFirefoxVerionPWD = getJsonData("winfirefoxList", FirefoxVersionList.get())
            if FirefoxVersionList.get() in winFirefoxDict:
                versionPWD = winFirefoxVerionPWD
            else:
                tkinter.messagebox.showwarning('警告', '程序字典中缺失该版本的键值')
        else:
            macFirefoxDict, macFirefoxVerionPWD = getJsonData("macfirefoxList", FirefoxVersionList.get())
            if FirefoxVersionList.get() in macFirefoxDict:
                versionPWD = macFirefoxVerionPWD
            else:
                tkinter.messagebox.showwarning('警告', '程序字典中缺失该版本的键值')
        if os.path.exists(versionPWD):
            try:
                if platform.system() == "Windows":
                    state = execInstallCMD(versionPWD)
                else:
                    state = execInstallCMD_MACOS(versionPWD,"Firefox")
                if state == False:
                    tkinter.messagebox.showerror('错误', '安装失败')
                else:
                    tkinter.messagebox.showinfo('提示', '安装成功')
            except:
                tkinter.messagebox.showerror('错误', '安装失败')
        else:
            tkinter.messagebox.showwarning('警告', '这个版本的安装包不存在')

def clickMeUninstallChrome():
    if platform.system() == "Windows":
        state = execUninstallChromeCMD()
    else:
        state = execUninstallChromeCMD_MACOS()
    if state == False:
        # uninstallChromeAction.configure(text='Uninstall fail ')
        tkinter.messagebox.showerror('错误', '卸载失败')
    elif state == "cancle":
        pass
    else:
        tkinter.messagebox.showinfo('提示', '卸载成功')
        # uninstallChromeAction.configure(text='Uninstall successed ')  # 设置button显示的内容
        # uninstallChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态

def clickMeUninstallFirefox():
    if platform.system() == "Windows":
        state = execUninstallFirefoxCMD()
    else:
        state = execUninstallFirefoxCMD__MACOS()
    if state == False:
        tkinter.messagebox.showerror('错误', '卸载失败')
        # uninstallFirefoxAction.configure(text='Uninstall fail ')
    elif state == "cancle":
        pass
    else:
        tkinter.messagebox.showinfo('提示', '卸载成功')
        # uninstallFirefoxAction.configure(text='Uninstall successed ')  # 设置button显示的内容
        # uninstallFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态

def clickOpenChrome():
    if sendChromeAddress.get() != "":
        if re.match("http",sendChromeAddress.get()):
            packagePWD = downloadPackage(sendChromeAddress.get())
            try:
                state = execOpenBrowser_MACOS(packagePWD,"Chrome")
                if state == False:
                    tkinter.messagebox.showerror('错误', '打开失败')
                else:
                    tkinter.messagebox.showinfo('提示', '打开成功')
            except:
                tkinter.messagebox.showerror('错误', '打开失败')
        else:
            try:
                state = execOpenBrowser_MACOS(sendChromeAddress.get(), "Chrome")
                if state == False:
                    tkinter.messagebox.showerror('错误', '打开失败')
                else:
                    tkinter.messagebox.showinfo('提示', '打开成功')
            except:
                tkinter.messagebox.showerror('错误', '打开失败')
    else:
        versionPWD = ""
        macChromeDict, macChromeVerionPWD = getJsonData("macchromeList", ChromeVersionList.get())
        if ChromeVersionList.get() in macChromeDict:
            versionPWD = macChromeVerionPWD
        else:
            tkinter.messagebox.showwarning('警告', '程序字典中缺失该版本的键值')
        if os.path.exists(versionPWD):
            try:
                state = execOpenBrowser_MACOS(versionPWD, "Chrome")
                if state == False:
                    tkinter.messagebox.showerror('错误', '打开失败')
                else:
                    tkinter.messagebox.showinfo('提示', '打开成功')
            except:
                tkinter.messagebox.showerror('错误', '打开失败')
        else:
            tkinter.messagebox.showwarning('警告', '这个版本的安装包不存在')
def clickOpenFirefox():
    if sendFirefoxAddress.get() != "":
        if re.match("http",sendFirefoxAddress.get()):
            packagePWD = downloadPackage(sendFirefoxAddress.get())
            try:
                state = execOpenBrowser_MACOS(packagePWD,"Firefox")
                if state == False:
                    tkinter.messagebox.showerror('错误', '打开失败')
                else:
                    tkinter.messagebox.showinfo('提示', '打开成功')
            except:
                tkinter.messagebox.showerror('错误', '打开失败')
        else:
            try:
                state = execOpenBrowser_MACOS(sendFirefoxAddress.get(), "Firefox")
                if state == False:
                    tkinter.messagebox.showerror('错误', '打开失败')
                else:
                    tkinter.messagebox.showinfo('提示', '打开成功')
            except:
                tkinter.messagebox.showerror('错误', '打开失败')
    else:
        versionPWD = ""
        macFirefoxDict, macFirefoxVerionPWD = getJsonData("macfirefoxList", FirefoxVersionList.get())
        if FirefoxVersionList.get() in macFirefoxDict:
            versionPWD = macFirefoxVerionPWD
        else:
            tkinter.messagebox.showwarning('警告', '程序字典中缺失该版本的键值')
        if os.path.exists(versionPWD):
            try:
                state = execOpenBrowser_MACOS(versionPWD, "Firefox")
                if state == False:
                    tkinter.messagebox.showerror('错误', '打开失败')
                else:
                    tkinter.messagebox.showinfo('提示', '打开成功')
            except:
                tkinter.messagebox.showerror('错误', '打开失败')
        else:
            tkinter.messagebox.showwarning('警告', '这个版本的安装包不存在')
def clickCloseChrome():
    state = execCloseBrowser_MACOS("Chrome")
    if state == False:
        tkinter.messagebox.showerror('错误', '关闭失败')
    else:
        tkinter.messagebox.showinfo('提示', '关闭成功')
def clickCloseFirefox():
    state = execCloseBrowser_MACOS("Firefox")
    if state == False:
        tkinter.messagebox.showerror('错误', '关闭失败')
    else:
        tkinter.messagebox.showinfo('提示', '关闭成功')


win = tk.Tk()
win.title("Agora Install Application")  # 添加标题

ttk.Label(win, text="Send the address of the browser installation package ").grid(column=0, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行
ttk.Label(win, text="Select a version").grid(column=1, row=0)  # 添加一个标签，并将其列设置为1，行设置为0

# 按钮
installChromeAction = ttk.Button(win, text="Install Chrome", command=clickMeInstallChrome)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
installChromeAction.grid(column=2, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
# 按钮2
installFirefoxAction = ttk.Button(win, text="Install Firefox  ", command=clickMeInstallFirefox)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
installFirefoxAction.grid(column=2, row=2)  # 设置其在界面中出现的位置  column代表列   row 代表行
# 按钮3
uninstallChromeAction = ttk.Button(win, text="Uninstall Chrome", command=clickMeUninstallChrome)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
uninstallChromeAction.grid(column=3, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
# 按钮4
uninstallFirefoxAction = ttk.Button(win, text="Uninstall Firefox  ", command=clickMeUninstallFirefox)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
uninstallFirefoxAction.grid(column=3, row=2)  # 设置其在界面中出现的位置  column代表列   row 代表行

# # openChrome
# openChromeAction = ttk.Button(win, text="Open Mac Chrome", command=clickOpenChrome)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
# openChromeAction.grid(column=4, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
# # openFirefox
# openFirefoxAction = ttk.Button(win, text="Open Mac Firefox  ", command=clickOpenFirefox)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
# openFirefoxAction.grid(column=4, row=2)  # 设置其在界面中出现的位置  column代表列   row 代表行
# # closeChrome
# closeChromeAction = ttk.Button(win, text="Close Mac Chrome", command=clickCloseChrome)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
# closeChromeAction.grid(column=5, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
# # closeFirefox
# closeFirefoxAction = ttk.Button(win, text="Close Mac Firefox  ", command=clickCloseFirefox)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
# closeFirefoxAction.grid(column=5, row=2)  # 设置其在界面中出现的位置  column代表列   row 代表行


# 文本框
sendChromeAddress = tk.StringVar()  # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
chromeAddressEntered = ttk.Entry(win, width=40, textvariable=sendChromeAddress)  # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
chromeAddressEntered.grid(column=0, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
chromeAddressEntered.focus()  # 当程序运行时,光标默认会出现在该文本框中
# 文本框2
sendFirefoxAddress = tk.StringVar()  # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
firefoxAddressEntered = ttk.Entry(win, width=40, textvariable=sendFirefoxAddress)  # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
firefoxAddressEntered.grid(column=0, row=2)  # 设置其在界面中出现的位置  column代表列   row 代表行
firefoxAddressEntered.focus()  # 当程序运行时,光标默认会出现在该文本框中

# 创建一个下拉列表
ChromeVersionList = tk.StringVar()
chromeVersionChosen = ttk.Combobox(win, width=10, textvariable=ChromeVersionList)
chromeVersionChosen['values'] = (49, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69)  # 设置下拉列表的值
chromeVersionChosen.grid(column=1, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
chromeVersionChosen.current(0)  # 设置下拉列表默认显示的值，0为 chromeVersionChosen['values'] 的下标值
# 创建一个下拉列表2
FirefoxVersionList = tk.StringVar()
firefoxVersionChosen = ttk.Combobox(win, width=10, textvariable=FirefoxVersionList)
firefoxVersionChosen['values'] = (56, 57, 58, 59, 60, 61, 62, 63, 64)  # 设置下拉列表的值
firefoxVersionChosen.grid(column=1, row=2)  # 设置其在界面中出现的位置  column代表列   row 代表行
firefoxVersionChosen.current(0)  # 设置下拉列表默认显示的值，0为 firefoxVersionChosen['values'] 的下标值

win.mainloop()