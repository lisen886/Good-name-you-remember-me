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

#-------------------------------   Windows   ---------------------------------------#

def execInstallWinCMD(pwd):
    cmd = "start /wait "+pwd+" /S"
    f = os.system(cmd)
    if str(f) != "0":
        return False

def install_chrome_on_win(browserPackage,useDicTag=False):
    if re.match("http",browserPackage):
        packagePWD = downloadPackage(browserPackage)
        try:
            state = execInstallWinCMD(packagePWD)
            if state == False:
                print("use http way to install failed")
            else:
                print("use http way to install success")
        except:
            print("use http way to install failed ")
    elif useDicTag is True :
        versionPWD = getJsonData("winchromeList")[browserPackage]
        print(versionPWD)
        # if str(browserPackage) in macChromeDict:
        try:
            pwd = os.getcwd()
            cmd = "start /wait " + pwd + versionPWD + " /S"
            f = os.system(cmd)
            if str(f) != "0":
                print("use exe to install failed")
            else:
                print("use exe to install successed")
        except:
            print("use exe to install failed")
    else:
        try:
            state = execInstallWinCMD(browserPackage)
            if state == False:
                print("use location station to install failed")
            else:
                print("use location station to install success")
        except:
            print("use location station to install failed")

def install_firefox_on_win(browserPackage,useDicTag=False):
    if re.match("http",browserPackage):
        packagePWD = downloadPackage(browserPackage)
        try:
            state = execInstallWinCMD(packagePWD)
            if state == False:
                print("use http way to install failed")
            else:
                print("use http way to install success")
        except:
            print("use http way to install failed ")
    elif useDicTag is True :
        versionPWD = getJsonData("winfirefoxList")[browserPackage]
        # if str(browserPackage) in macChromeDict:
        try:
            pwd = os.getcwd()
            cmd = "start /wait " + pwd + versionPWD + " /S"
            f = os.system(cmd)
            if str(f) != "0":
                print("use exe to install failed")
            else:
                print("use exe to install successed")
        except:
            print("use exe to install failed")
    else:
        try:
            state = execInstallWinCMD(browserPackage)
            if state == False:
                print("use location station to install failed")
            else:
                print("use location station to install success")
        except:
            print("use location station to install failed")

def uninstall_chrome_on_win():
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

def uninstall_firefox_on_win():
    cmd = r'"C:\Program Files\Mozilla Firefox\uninstall\helper.exe" /S'
    f = os.system(cmd)
    if str(f) != "0":
        return False
    else:
        print("firfox uninstall success")

#-------------------------------   MAC ---------------------------------------#

def install_chrome_on_mac(browserPackage,UseDicTag=False):
    if re.match("http",browserPackage):
        packagePWD = downloadPackage(browserPackage)
        try:
            state = exec_install_cmd_on_mac(packagePWD,Btype="Chrome")
            if state == False:
                print("use http way to install failed")
            else:
                print("use http way to install success")
        except:
            print("use http way to install failed ")
    elif UseDicTag is True :
        versionPWD = getJsonData("macchromeList")[browserPackage]
        print(versionPWD)
        # if str(browserPackage) in macChromeDict:
        try:
            state = exec_install_cmd_on_mac(versionPWD, Btype="Chrome")
            if state == False:
                print("use dic to install failed")
            else:
                print("use dic to install success")
        except:
            print("version not exit")
    else:
        try:
            state = exec_install_cmd_on_mac(browserPackage,Btype="Chrome")
            if state == False:
                print("use location station to install failed")
            else:
                print("use location station to install success")
        except:
            print("use location station to install failed")


def install_firefox_on_mac(browserPackage,UseDicTag=False):
    if re.match("http",browserPackage):
        packagePWD = downloadPackage(browserPackage)
        try:
            state = exec_install_cmd_on_mac(packagePWD,Btype="Firefox")
            if state == False:
                print("use http way to install failed")
            else:
                print("use http way to install success")
        except:
            print("use http way to install failed ")
    elif UseDicTag is True :
        versionPWD = getJsonData("macfirefoxList")[browserPackage]
        print(versionPWD)
        # if str(browserPackage) in macChromeDict:
        try:
            state = exec_install_cmd_on_mac(versionPWD, Btype="Firefox")
            if state == False:
                print("use dic to install failed")
            else:
                print("use dic to install success")
        except:
            print("version not exit")
    else:
        try:
            state = exec_install_cmd_on_mac(browserPackage,Btype="Firefox")
            if state == False:
                print("use location station to install failed")
            else:
                print("use location station to install success")
        except:
            print("use location station to install failed")

def exec_install_cmd_on_mac(pwd,Btype):
    attachCMD = "hdiutil attach " + pwd
    out = os.system(attachCMD)
    if Btype == "Chrome":
        os.system("rm -rf /Applications/Google\ Chrome.app/")
        os.system("cp -r /Volumes/Google\ Chrome/Google\ Chrome.app/ /Applications/Google\ Chrome.app/")
        os.system("hdiutil detach /Volumes/Google\ Chrome/")
        print ("install Chrome success ")
    elif Btype == "Firefox":
        os.system("rm -rf /Applications/Firefox.app/")
        os.system("cp -r /Volumes/Firefox/Firefox.app/ /Applications/Firefox.app/")
        os.system("hdiutil detach /Volumes/Firefox/")
        print ("install Firefox success")
    else:
        print("unsupport this browser to install")

def uninstall_chrome_on_mac():
    cmd = "rm -rf /Applications/Google\ Chrome.app/"
    f = os.system(cmd)
    if str(f) != "0":
        print("uninstall mac_chrome failed")
        return False
    else:
        print("uninstall mac_chrome sucsess")

def uninstall_firefox_on_mac():
    cmd = "rm -rf /Applications/Firefox.app/"
    f = os.system(cmd)
    if str(f) != "0":
        print("uninstall mac_firefox failed")
        return False
    else:
        print("uninstall mac_firefox success")

def downloadPackage(url):
    # http://10.80.0.160:8888/Firefox60.0.exe
    # packageName = url.split("/")[-1]
    # packagePWD = os.getcwd() + "\\" + packageName
    # if sys.version < "3":
    #     f = urllib2.urlopen(url)
    #     data = f.read()
    #     with open(packageName, "wb") as code:
    #         code.write(data)
    # else:
    #     request.urlretrieve(url,"./%s"%packageName)
    # return packagePWD
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

def getJsonData(browserType):
    with open("./browserConfig.json","r") as load_f:
        load_dict = json.load(load_f)
        return load_dict[browserType]
if __name__ == "__main__":
    print("test interface")
    # install_chrome_on_mac("http://10.80.0.160:8888/AgoraMacInstall/chrome/49.0.2623.13_chrome64_dev_osx_installer.dmg")
    # install_chrome_on_mac("/tmp/49.0.2623.13_chrome64_dev_osx_installer.dmg")
    # install_chrome_on_mac(browserPackage="49",UseDicTag=True)
    # uninstall_chrome_on_mac()
    # install_firefox_on_mac("http://10.80.0.160:8888/AgoraMacInstall/firefox/Firefox63.0.dmg")
    # install_firefox_on_mac("/tmp/Firefox63.0.dmg")
    # uninstall_firefox_on_mac()

    # uninstall_chrome_on_win()
    # install_chrome_on_win("http://10.80.0.160:8888/AgoraWinInstall/chrome/69.0.3497.81_chrome64_stable_windows_installer.exe")
    # install_chrome_on_win("D:\\test_install\\69.0.3497.81_chrome64_stable_windows_installer.exe")
    # install_chrome_on_win("69",useDicTag=True)

    # uninstall_firefox_on_win()
    # install_firefox_on_win("http://10.80.0.160:8888/AgoraWinInstall/firefox/Firefox63.0.exe")
    # install_firefox_on_win("60",useDicTag=True)
    install_firefox_on_win("D:\\test_install\\FirefoxSetup64.0b4.exe")