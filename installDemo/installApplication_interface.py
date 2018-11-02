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
chrome = {
    "49":r".\chrome\49.0.2623.75_chrome64_stable_windows_installer.exe",
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
    "69":r".\chrome\69.0.3497.81_chrome64_stable_windows_installer.exe"
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

mac_chrome = {
    "49":r"./49.0.2623.13_chrome64_dev_osx_installer.dmg"
}
mac_firefox = {
    "56":r"./Firefox56.0.dmg",
    "57":r"./Firefox57.0.dmg",
    "58":r"./Firefox58.0.dmg",
    "59":r"./Firefox59.0.dmg",
    "60":r"./Firefox60.0.dmg",
    "61":r"./Firefox61.0.dmg",
    "62":r"./Firefox62.0.dmg",
    "63":r"./Firefox63.0.dmg",
    "64":r"./Firefox64.0b5.dmg"
}

def execInstallWinCMD(pwd):
    cmd = "start /wait "+pwd+" /S"
    f = os.system(cmd)
    if str(f) != "0":
        return False

def install_on_win(browserPackage):
    if browserPackage != "":
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
        else:
            try:
                state = execInstallWinCMD(browserPackage)
                if state == False:
                    print("use location station to install failed")
                else:
                    print("use location station to install success")
            except:
                print("use location station to install failed")
    else:
        if str(browserPackage) in chrome:
            versionPWD = chrome[str(browserPackage)]
            if os.path.exists(versionPWD):
                try:
                    state = execInstallWinCMD(versionPWD)
                    if state == False:
                        print("use exe to install failed")
                    else:
                        print("use exe to install successed")
                except:
                    print("use exe to install failed")
            else:
                print("This version of the file does not exist")
        else:
            print("The dict is missing this value")

def uninstall_chrome():
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

def uninstall_firefox():
    cmd = r'"C:\Program Files\Mozilla Firefox\uninstall\helper.exe" /S'
    print("exec:", cmd)
    f = os.system(cmd)
    if str(f) != "0":
        return False
    else:
        print("firfox uninstall success")

################### MAC ###################################################

def install_chrome_on_mac(browserPackage):
    if browserPackage != "":
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
        else:
            try:
                state = exec_install_cmd_on_mac(browserPackage,Btype="Chrome")
                if state == False:
                    print("use location station to install failed")
                else:
                    print("use location station to install success")
            except:
                print("use location station to install failed")
    else:
        if str(browserPackage) in mac_chrome:
            versionPWD = mac_chrome[str(browserPackage)]
            if os.path.exists(versionPWD):
                try:
                    state = exec_install_cmd_on_mac(versionPWD,Btype="Chrome")
                    if state == False:
                        print("use exe to install failed")
                    else:
                        print("use exe to install successed")
                except:
                    print("use exe to install failed")
            else:
                print("This version of the file does not exist")
        else:
            print("The dict is missing this value")

def install_firefox_on_mac(browserPackage):
    if browserPackage != "":
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
        else:
            try:
                state = exec_install_cmd_on_mac(browserPackage,Btype="Firefox")
                if state == False:
                    print("use location station to install failed")
                else:
                    print("use location station to install success")
            except:
                print("use location station to install failed")
    else:
        if str(browserPackage) in mac_firefox:
            versionPWD = mac_firefox[str(browserPackage)]
            if os.path.exists(versionPWD):
                try:
                    state = exec_install_cmd_on_mac(versionPWD,Btype="Firefox")
                    if state == False:
                        print("use dic to install failed")
                    else:
                        print("use dic to install successed")
                except:
                    print("use dic to install failed")
            else:
                print("This version of the file does not exist")
        else:
            print("The dict is missing this value")

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

def getJsonData(browserType,version):
    with open("./browserConfig.json","r") as load_f:
        load_dict = json.load(load_f)
        print(load_dict[browserType][str(version)])
if __name__ == "__main__":
    print("test interface")
    # install_chrome_on_mac("http://10.80.0.160:8888/AgoraMacInstall/chrome/49.0.2623.13_chrome64_dev_osx_installer.dmg")
    # install_chrome_on_mac("/tmp/49.0.2623.13_chrome64_dev_osx_installer.dmg")
    # uninstall_chrome_on_mac()
    # install_firefox_on_mac("http://10.80.0.160:8888/AgoraMacInstall/firefox/Firefox63.0.dmg")
    # install_firefox_on_mac("/tmp/Firefox63.0.dmg")
    # uninstall_firefox_on_mac()
    getJsonData("winchromeList","59")