#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import os,re,sys
if sys.version < "3":
    import urllib2
else:
    # 因为打包程序没法使用urllib，改用urllib2
    from urllib import request
chrome = {
    "49":r".\49.0.2623.75_chrome64_stable_windows_installer.exe",
    "70":r".\ChromeSetup.exe"
}
firefox = {
    "50":r".\Firefox60.0.exe"
}
def execInstallCMD(pwd):
    cmd = "start /wait "+pwd+" /S"
    f = os.system(cmd)
    if str(f) != "0":
        return False

def execUninstallFirefoxCMD():
    cmd = r'"C:\Program Files\Mozilla Firefox\uninstall\helper.exe" /S'
    f = os.system(cmd)
    if str(f) != "0":
        return False

def execUninstallChromeCMD():
    get_version_cmd = r'wmic datafile where name="C:\\Users\\%Username%\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe" get Version /value > D:\\a.txt"'
    os.system(get_version_cmd)
    f = open('D:/a.txt',encoding='utf-16')
    txtcont = f.read()
    f.close()
    print (txtcont[10:22])
    chrome_version = txtcont[10:22]
    uninstallchrome_cmd = "C:\\Users\\%Username%\\AppData\\Local\\Google\\Chrome\\Application\\" + chrome_version + "\\Installer\\setup.exe --uninstall --multi-install --chrome"
    f = os.system(uninstallchrome_cmd)
    if str(f) != "0":
        return False

def downloadPackage(url):
    # http://10.80.0.160:8888/Firefox60.0.exe
    packageName = sendChromeAddress.get().split("/")[-1]
    packagePWD = os.getcwd() + "\\" + packageName
    if sys.version < "3":
        f = urllib2.urlopen(url)
        data = f.read()
        with open(packageName, "wb") as code:
            code.write(data)
    else:
        request.urlretrieve(url,"./%s"%packageName)
    return packagePWD
# def clickMeInstallChrome():  # 当acction被点击时,该函数则生效
#     if sendChromeAddress.get() != "":
#         try:
#             state = execInstallCMD(sendChromeAddress.get())
#             if state == False:
#                 installChromeAction.configure(text='Install fail ')
#             else:
#                 installChromeAction.configure(text='Install successed ')  # 设置button显示的内容
#                 installChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
#         except:
#             installChromeAction.configure(text='Install fail ')
#     else:
#         if ChromeVersionList.get() in chrome:
#             versionPWD = chrome[ChromeVersionList.get()]
#             if os.path.exists(versionPWD):
#                 try:
#                     state = execInstallCMD(versionPWD)
#                     if state == False:
#                         installChromeAction.configure(text='Install fail ')
#                     else:
#                         installChromeAction.configure(text='Install successed ')  # 设置button显示的内容
#                         installChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
#                 except:
#                     installChromeAction.configure(text='Install fail ')
#             else:
#                 installChromeAction.configure(text='This version of the file does not exist.')
#         else:
#             installChromeAction.configure(text='The dict is missing this value')
def clickMeInstallChrome():  # 当acction被点击时,该函数则生效
    if sendChromeAddress.get() != "":
        if re.match("http",sendChromeAddress.get()):
            packagePWD = downloadPackage(sendChromeAddress.get())
            try:
                state = execInstallCMD(packagePWD)
                if state == False:
                    installChromeAction.configure(text='Install fail ')
                else:
                    installChromeAction.configure(text='Install successed ')  # 设置button显示的内容
                    installChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
            except:
                installChromeAction.configure(text='Install fail ')
        else:
            try:
                state = execInstallCMD(sendChromeAddress.get())
                if state == False:
                    installChromeAction.configure(text='Install fail ')
                else:
                    installChromeAction.configure(text='Install successed ')  # 设置button显示的内容
                    installChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
            except:
                installChromeAction.configure(text='Install fail ')
    else:
        if ChromeVersionList.get() in chrome:
            versionPWD = chrome[ChromeVersionList.get()]
            if os.path.exists(versionPWD):
                try:
                    state = execInstallCMD(versionPWD)
                    if state == False:
                        installChromeAction.configure(text='Install fail ')
                    else:
                        installChromeAction.configure(text='Install successed ')  # 设置button显示的内容
                        installChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
                except:
                    installChromeAction.configure(text='Install fail ')
            else:
                installChromeAction.configure(text='This version of the file does not exist.')
        else:
            installChromeAction.configure(text='The dict is missing this value')
def clickMeInstallFirefox():  # 当acction被点击时,该函数则生效
    if sendFirefoxAddress.get() != "":
        if re.match("http",sendFirefoxAddress.get()):
            packagePWD = downloadPackage(sendFirefoxAddress.get())
            try:
                state = execInstallCMD(packagePWD)
                if state == False:
                    installFirefoxAction.configure(text='Install fail ')
                else:
                    installFirefoxAction.configure(text='Install successed ')  # 设置button显示的内容
                    installFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
            except:
                installFirefoxAction.configure(text='Install fail ')
        else:
            try:
                state = execInstallCMD(sendFirefoxAddress.get())
                if state == False:
                    installFirefoxAction.configure(text='Install fail ')
                else:
                    installFirefoxAction.configure(text='Install successed ')  # 设置button显示的内容
                    installFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
            except:
                installFirefoxAction.configure(text='Install fail ')
    else:
        if FirefoxVersionList.get() in firefox:
            versionPWD = firefox[FirefoxVersionList.get()]
            if os.path.exists(versionPWD):
                try:
                    state = execInstallCMD(versionPWD)
                    if state == False:
                        installFirefoxAction.configure(text='Install fail ')
                    else:
                        installFirefoxAction.configure(text='Install successed ')  # 设置button显示的内容
                        installFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
                except:
                    installFirefoxAction.configure(text='Install fail ')
            else:
                installFirefoxAction.configure(text='This version of the file does not exist.')
        else:
            installFirefoxAction.configure(text='The dict is missing this value')

def clickMeUninstallChrome():
    state = execUninstallChromeCMD()
    if state == False:
        uninstallChromeAction.configure(text='Uninstall fail ')
    else:
        uninstallChromeAction.configure(text='Uninstall successed ')  # 设置button显示的内容
        uninstallChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态

def clickMeUninstallFirefox():
    state = execUninstallFirefoxCMD()
    if state == False:
        uninstallFirefoxAction.configure(text='Uninstall fail ')
    else:
        uninstallFirefoxAction.configure(text='Uninstall successed ')  # 设置button显示的内容
        uninstallFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态

win = tk.Tk()
win.title("Install Application")  # 添加标题

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
chromeVersionChosen['values'] = (49, 50, 51, 52, 53, 70)  # 设置下拉列表的值
chromeVersionChosen.grid(column=1, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
chromeVersionChosen.current(0)  # 设置下拉列表默认显示的值，0为 chromeVersionChosen['values'] 的下标值
# 创建一个下拉列表2
FirefoxVersionList = tk.StringVar()
firefoxVersionChosen = ttk.Combobox(win, width=10, textvariable=FirefoxVersionList)
firefoxVersionChosen['values'] = (49, 50, 51, 52, 53, 70)  # 设置下拉列表的值
firefoxVersionChosen.grid(column=1, row=2)  # 设置其在界面中出现的位置  column代表列   row 代表行
firefoxVersionChosen.current(0)  # 设置下拉列表默认显示的值，0为 firefoxVersionChosen['values'] 的下标值

win.mainloop()