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

def execInstallCMD(pwd):
    cmd = "start /wait "+pwd+" /S"
    f = os.system(cmd)
    if str(f) != "0":
        return False

def install_function(browserPackage):
    if browserPackage != "":
        if re.match("http",browserPackage):
            packagePWD = downloadPackage(browserPackage)
            try:
                state = execInstallCMD(packagePWD)
                if state == False:
                    print("use http way to install failed")
                else:
                    print("use http way to install success")
            except:
                print("use http way to install failed ")
        else:
            try:
                state = execInstallCMD(browserPackage)
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
                    state = execInstallCMD(versionPWD)
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
    f = os.system(cmd)
    if str(f) != "0":
        return False

def downloadPackage(url):
    # http://10.80.0.160:8888/Firefox60.0.exe
    packageName = url.get().split("/")[-1]
    packagePWD = os.getcwd() + "\\" + packageName
    if sys.version < "3":
        f = urllib2.urlopen(url)
        data = f.read()
        with open(packageName, "wb") as code:
            code.write(data)
    else:
        request.urlretrieve(url,"./%s"%packageName)
    return packagePWD