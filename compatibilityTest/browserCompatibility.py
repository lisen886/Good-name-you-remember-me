#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from installApplication_interface import *

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
    webdriverPwd = getJson(browserType, version)
    closeProcess(browserType)
    driver =""
    if browserType == "macchrome":
        os.environ["webdriver.Chrome.driver"] = webdriverPwd

        macoption = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values.media_stream_camera': 1,
                 'profile.default_content_setting_values.media_stream_mic': 1,
                 'profile.default_content_setting_values.notifications': 1,
                 'profile.default_content_setting_values.geolocation': 1}
        macoption.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(executable_path=webdriverPwd, chrome_options=macoption)
        printMy(driver.capabilities['version'])
    elif browserType == "macfirefox":
        os.environ["webdriver.Firefox.driver"] = webdriverPwd
        macprofile = webdriver.FirefoxProfile()
        macprofile.set_preference('media.navigator.permission.disabled', True)
        macprofile.update_preferences()
        driver = webdriver.Firefox(executable_path=webdriverPwd, firefox_profile=macprofile)
        printMy(driver.capabilities['browserVersion'])
    elif browserType == "winchrome":
        os.environ["webdriver.Chrome.driver"] = webdriverPwd
        winoption = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values.media_stream_camera': 1,
                 'profile.default_content_setting_values.media_stream_mic': 1,
                 'profile.default_content_setting_values.notifications': 1,
                 'profile.default_content_setting_values.geolocation': 1}
        winoption.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(executable_path=webdriverPwd, chrome_options=winoption)
        printMy(driver.capabilities['version'])
    elif browserType == "winfirefox":
        os.environ["webdriver.Firefox.driver"] = webdriverPwd
        winprofile = webdriver.FirefoxProfile()
        winprofile.set_preference('media.navigator.permission.disabled', True)
        winprofile.update_preferences()
        driver = webdriver.Firefox(executable_path=webdriverPwd, firefox_profile=winprofile)
        printMy(driver.capabilities['browserVersion'])
    return driver

def printMy(String):
    print('\033[1;35m%s \033[0m!'%String)

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
        uninstall_chrome_on_win()
        install_chrome_on_win(version)
        testCase(browserType,version)
    elif browserType == "winfirefox":
        uninstall_firefox_on_win()
        install_firefox_on_win(version)
        testCase(browserType, version)

if __name__ == '__main__':
    # main("winchrome","68")
    # main("winchrome","69")
    # main("winfirefox","63")
    # main("winfirefox","64")
    main("macchrome","68")
    main("macchrome","69")
    main("macfirefox","63")
    main("macfirefox","64")