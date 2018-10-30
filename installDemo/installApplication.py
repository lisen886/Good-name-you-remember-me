#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import os,re,sys
if sys.version < "3":
    import urllib2
else:
    # 因为打包程序没法使用urllib，改用urllib2
    from urllib import request
chrome = {
    "49":r".\49.0.2623.75_chrome64_stable_windows_installer.exe",
    "58":r".\58.0.3029.81_chrome64_stable_windows_installer.exe",
    "59":r".\59.0.3071.25_chrome64_dev_windows_installer.exe",
    "60":r".\60.0.3112.113_chrome64_stable_windows_installer.exe",
    "61":r".\61.0.3163.79_chrome64_stable_windows_installer.exe",
    "62":r".\62.0.3202.62_chrome64_stable_windows_installer.exe",
    "63":r".\63.0.3239.132_chrome64_stable_windows_installer.exe",
    "64":r".\64.0.3282.140_chrome64_stable_windows_installer.exe",
    "65":r".\65.0.3325.162_chrome64_stable_windows_installer.exe",
    "66":r".\66.0.3359.139_chrome64_stable_windows_installer.exe",
    "67":r".\67.0.3396.87_chrome64_stable_windows_installer.exe",
    "68":r".\68.0.3440.106_chrome64_stable_windows_installer.exe",
    "69":r".\69.0.3497.81_chrome64_stable_windows_installer.exe"
}
firefox = {
    "56":r".\Firefox56.0.exe",
    "57":r".\Firefox57.0.exe",
    "58":r".\Firefox58.0.exe",
    "59":r".\Firefox59.0.exe",
    "60":r".\Firefox60.0.exe",
    "61":r".\Firefox61.0.exe",
    "62":r".\Firefox62.0.exe",
    "63":r".\Firefox63.0.exe",
    "64":r".\Firefox64.0b5.exe"
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
    os.system("taskkill /F /IM chrome.exe /T")
    get_version_cmd = r'wmic datafile where name="C:\\Users\\%Username%\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe" get Version /value'
    f = os.popen(get_version_cmd)
    out = f.read()
    f.close()
    chrome_version = out.split("=")[-1].strip()
    uninstallchrome_cmd = "C:\\Users\\%Username%\\AppData\\Local\\Google\\Chrome\\Application\\" + str(chrome_version) + "\\Installer\\setup.exe --uninstall --multi-install --chrome"
    f = os.system(uninstallchrome_cmd)
    print(f)
    if str(f) != "0" and str(f) != "19":
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
def clickMeInstallChrome():  # 当acction被点击时,该函数则生效
    if sendChromeAddress.get() != "":
        if re.match("http",sendChromeAddress.get()):
            packagePWD = downloadPackage(sendChromeAddress.get())
            try:
                state = execInstallCMD(packagePWD)
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
            try:
                state = execInstallCMD(sendChromeAddress.get())
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
        if ChromeVersionList.get() in chrome:
            versionPWD = chrome[ChromeVersionList.get()]
            if os.path.exists(versionPWD):
                try:
                    state = execInstallCMD(versionPWD)
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
                tkinter.messagebox.showwarning('警告', '这个版本的安装包不存在')
                # installChromeAction.configure(text='This version of the file does not exist.')
        else:
            tkinter.messagebox.showwarning('警告', '程序字典中缺失该版本的键值')
            # installChromeAction.configure(text='The dict is missing this value')
def clickMeInstallFirefox():  # 当acction被点击时,该函数则生效
    if sendFirefoxAddress.get() != "":
        if re.match("http",sendFirefoxAddress.get()):
            packagePWD = downloadPackage(sendFirefoxAddress.get())
            try:
                state = execInstallCMD(packagePWD)
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
        else:
            try:
                state = execInstallCMD(sendFirefoxAddress.get())
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
        if FirefoxVersionList.get() in firefox:
            versionPWD = firefox[FirefoxVersionList.get()]
            if os.path.exists(versionPWD):
                try:
                    state = execInstallCMD(versionPWD)
                    if state == False:
                        # installFirefoxAction.configure(text='Install fail ')
                        tkinter.messagebox.showerror('错误', '安装失败')
                    else:
                        tkinter.messagebox.showinfo('提示', '安装成功')
                        # installFirefoxAction.configure(text='Install successed ')  # 设置button显示的内容
                        # installFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态
                except:
                    # installFirefoxAction.configure(text='Install fail ')
                    tkinter.messagebox.showerror('错误', '安装失败')
            else:
                tkinter.messagebox.showwarning('警告', '这个版本的安装包不存在')
                # installFirefoxAction.configure(text='This version of the file does not exist.')
        else:
            tkinter.messagebox.showwarning('警告', '程序字典中缺失该版本的键值')
            # installFirefoxAction.configure(text='The dict is missing this value')

def clickMeUninstallChrome():
    state = execUninstallChromeCMD()
    if state == False:
        # uninstallChromeAction.configure(text='Uninstall fail ')
        tkinter.messagebox.showerror('错误', '卸载失败')
    else:
        tkinter.messagebox.showinfo('提示', '卸载成功')
        # uninstallChromeAction.configure(text='Uninstall successed ')  # 设置button显示的内容
        # uninstallChromeAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态

def clickMeUninstallFirefox():
    state = execUninstallFirefoxCMD()
    if state == False:
        tkinter.messagebox.showerror('错误', '卸载失败')
        # uninstallFirefoxAction.configure(text='Uninstall fail ')
    else:
        tkinter.messagebox.showinfo('提示', '卸载成功')
        # uninstallFirefoxAction.configure(text='Uninstall successed ')  # 设置button显示的内容
        # uninstallFirefoxAction.configure(state='disabled')  # 将按钮设置为灰色状态，不可使用状态

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