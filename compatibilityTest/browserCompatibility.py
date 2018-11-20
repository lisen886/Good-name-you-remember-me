#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from installDemo.installApplication_interface import *

def getJson(browserType,version):
    try:
        jsonPWD = "./webdriverMap.json"
        if os.path.exists(jsonPWD):
            with open(jsonPWD,"r") as load_f:
                load_dict = json.load(load_f)
                appPWD = os.getcwd()
                if platform.system() == "Windows":
                    versionPWD = appPWD+load_dict[browserType][str(version)].replace("/", "\\")
                else:
                    versionPWD = appPWD + load_dict[browserType][str(version)]
                return versionPWD
        else:
            print('警告', '请将webdriverMap.json移到程序相同路径下')
    except:
        print('警告', 'json文件格式有问题或者键值对不存在')
def closeProcess(browserType):
    if browserType == "macchrome":
        os.system("ps -ef | grep " + "Google" + " | grep -v grep | awk '{print $2}' | xargs kill -9")
    elif browserType == "macfirefox":
        os.system("ps -ef | grep " + "Firefox" + " | grep -v grep | awk '{print $2}' | xargs kill -9")
    elif browserType == "winchrome":
        os.system("taskkill /f /im " + "Chrome" + ".exe")
    elif browserType == "winfirefox":
        os.system("taskkill /f /im " + "Firefox" + ".exe")

def openBrowser(browserType,version):
    MacChromePath = "--user-data-dir=/Users/lisen/Library/Application Support/Google/Chrome"
    MacFirefoxPath = "/Users/lisen/Library/Application Support/Firefox/Profiles/28mwdrcp.default"
    WindowsChromePath = r"--user-data-dir=C:\Users\chacha\AppData\Local\Google\Chrome\User Data\Default"
    WindowsFirefoxPath = r"C:\Users\chacha\AppData\Local\Mozilla\Firefox\Profiles\79g1uvxi.default"
    webdriverPwd = getJson(browserType, version)
    closeProcess(browserType)
    driver =""
    if browserType == "macchrome":
        os.environ["webdriver.Chrome.driver"] = webdriverPwd
        macoption = webdriver.ChromeOptions()
        macoption.add_argument(MacChromePath)
        driver = webdriver.Chrome(executable_path=webdriverPwd, chrome_options=macoption)
    elif browserType == "macfirefox":
        os.environ["webdriver.Firefox.driver"] = webdriverPwd
        macfirefoxProfile = webdriver.FirefoxProfile(MacFirefoxPath)
        driver = webdriver.Firefox(executable_path=webdriverPwd, firefox_profile=macfirefoxProfile)
    elif browserType == "winchrome":
        os.environ["webdriver.Chrome.driver"] = webdriverPwd
        winoption = webdriver.ChromeOptions()
        winoption.add_argument(WindowsChromePath)
        driver = webdriver.Chrome(executable_path=webdriverPwd, chrome_options=winoption)
    elif browserType == "winfirefox":
        os.environ["webdriver.Firefox.driver"] = webdriverPwd
        winfirefoxProfile = webdriver.FirefoxProfile(WindowsFirefoxPath)
        driver = webdriver.Firefox(executable_path=webdriverPwd, firefox_profile=winfirefoxProfile)
    return driver

def testCase(browserType,version):
    driver = openBrowser(browserType,version)
    driver.get(
        "https://webdemo.agora.io/premium_rtc_test_2.5/show.html?channelName=asdsd&videoProfile=480p_4&uid=&uidtype=int&mode=live&codec=vp8&interop_mode=interop_commutication&avmode=0&dynamic=disabled&expiration=0&custom_key=&key=disabled&proxy=disabled&turnServerIP=113.207.108.198&udpPort=3478&tcpPort=3433&username=test&password=111111&forceTurn=disabled&nginxURL=webopt.agorabeckon.com&encrypt=disabled&encryptMode=none&encryptPassword=&preprocessing=disabled")
    time.sleep(5)
    driver.quit()

def main(browserType,version):
    if browserType == "macchrome":
        uninstall_chrome_on_mac()
        install_chrome_on_mac(version)
        testCase(browserType,version)
    elif browserType == "macfirefox":
        uninstall_firefox_on_mac()
        install_firefox_on_mac(version)
        testCase(browserType, version)
    elif browserType == "winchrome":
        uninstall_chrome_on_mac()
        install_chrome_on_mac(version)
        testCase(browserType,version)
    elif browserType == "winfirefox":
        uninstall_firefox_on_mac()
        install_firefox_on_mac(version)
        testCase(browserType, version)

def test(i):
    print(i)

if __name__ == '__main__':
    main("winchrome","66")
    main("winchrome","67")
    main("winchrome","68")
    main("winchrome","69")