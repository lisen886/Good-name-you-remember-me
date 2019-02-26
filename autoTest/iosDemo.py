# coding:utf-8
from appium import webdriver
import time
channelName = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
PUSHURL = time.strftime("%M%S", time.localtime())
desired_caps = {}
desired_caps['automationName'] = 'XCUITest'
desired_caps['platformName'] = 'iOS'
desired_caps['platformVersion'] = '11.2.2'
desired_caps['deviceName'] = 'iPadmini4'
desired_caps['bundleId'] = 'io.*****************.A*****************Premium'
desired_caps['udid'] = '162e308fc1a*****************ab78effe257ebebd'
desired_caps['newCommandTimeout'] = 3600

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

driver.find_element_by_id("channel_name").clear()
driver.find_element_by_id("channel_name").send_keys(channelName)
driver.find_element_by_id("Join").click()
time.sleep(5)
driver.find_element_by_id("btn close").click()
driver.quit()


# - 安装webDriverAgent：https://testerhome.com/topics/14911
#   * 我使用的是appium命令行，目录可能在/usr/local/lib/node_modules/
#     appium/node_modules/appium-xcuitest-driver/WebDriverAgent/WebDriverAgent.xcodeproj
#
# - 通过xcode->product->test install Demo to iPhone(SJ0144)
#
# - 查找元素：https://blog.csdn.net/wuyepiaoxue789/article/details/77859362
#
# - 启动：appium -p 4723