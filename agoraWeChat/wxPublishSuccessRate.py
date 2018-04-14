# python2
# -*- coding: UTF-8 -*-
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os,re,time
import subprocess
import base64

mp4cwd = os.getcwd()+"/wxPub.mp4"
# 为线程定义一个函数
def wx_publish_Success(num):
    PubfailName = []
    CannotJoinChannelName = []
    failNum = 0
    for i in range(105,num+1):
        inputChannelName = "slRejoinTest" + str(i)
        print (inputChannelName)
        base64Name = (str(base64.b64encode(inputChannelName)))
        cmd ="ffmpeg -re -stream_loop -1 -i "+mp4cwd+" -c copy -f flv rtmp://test.mini-app.broadcastapp.agoraio.cn/live/" \
             "f4637604af81440596a54254d53ade20_"+base64Name+"_12345678"
        # 只推视频  -c copy -an -f flv
        # cmd ="ffmpeg -re -stream_loop -1 -i "+mp4cwd+" -c copy -an -f flv rtmp://test.mini-app.broadcastapp.agoraio.cn/live/" \
        #      "f4637604af81440596a54254d53ade20_"+base64Name+"_12345678"
        sub =subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        # sub.wait()
        # print (sub.stdout.read())

        desired_caps = {}
        desired_caps['appium-version'] = '1.0'
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'bdf2115'
        desired_caps['appPackage'] = 'io.agora.premium'
        desired_caps['appActivity'] = '.ui.MainActivity'
        driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
        els = driver.find_elements_by_class_name('android.widget.Button')
        for el in els:
            if el.text == u'允许':
                driver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
            elif el.text == u'始终允许':
                driver.find_element_by_android_uiautomator('new UiSelector().text("始终允许")').click()
            elif el.text == u'确定':
                driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
        els2 = driver.find_elements_by_class_name('android.widget.Button')
        for el2 in els2:
            if el2.text == u'允许':
                driver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
            elif el2.text == u'始终允许':
                driver.find_element_by_android_uiautomator('new UiSelector().text("始终允许")').click()
            elif el2.text == u'确定':
                driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()

        ele = driver.find_element_by_id("use_new_app_id")
        attribute = ele.get_attribute("checked")
        if attribute == "true":
            ele.click()
        else:
            pass
        driver.find_element_by_id("channel_name").clear()
        driver.find_element_by_id("channel_name").send_keys(inputChannelName)
        driver.hide_keyboard("Return")
        driver.find_element_by_id("button_join").click()
        driver.find_element_by_id("button2").click()
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "audio_info_metadata")))
            time.sleep(4)
            info = driver.find_element_by_id("app_stats_info").text
            Audio_Bitrate_info = re.findall(r"rx(.*) V:", info)
            Audio_Bitrate = re.sub('[()]', '', Audio_Bitrate_info[0])
            Video_Bitrate_info = re.findall(r"V: tx(.*) All:", info)
            Video_Bitrate = re.sub('[()]', '', Video_Bitrate_info[0]).split("rx")[1]
            if int(Audio_Bitrate) > 0 and int(Video_Bitrate) > 0:
                cmdPS = "ps -au lisen | grep " + base64Name + " | awk '{print $2}'"
                ss = subprocess.Popen(cmdPS, shell=True, stdout=subprocess.PIPE)
                ss.wait()
                listP = ss.stdout.read().split("\n")
                for i in range(0, len(listP)):
                    cmd2 = "kill " + listP[i]
                    subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
            else:
                print ("this channelName: %s publish fail" % inputChannelName)
                print (info)
                PubfailName.append(inputChannelName)
                failNum += 1
            driver.find_element_by_id("bottom_action_end_call").click()
            driver.find_element_by_id("btn_rate_call").click()
        except:
            failNum += 1
            print ("this channelName: %s can't join channel" % inputChannelName)
            CannotJoinChannelName.append(inputChannelName)
        finally:
            driver.quit()
        print ("now fail num：%d" % failNum)
    print ("fail num：%d" % failNum)
    print (PubfailName,CannotJoinChannelName)
    rate = failNum / float(num)
    success_rate = (1 -rate)*100
    print ("publish success rate is %f" % success_rate)

if __name__ == '__main__':
    wx_publish_Success(500)

