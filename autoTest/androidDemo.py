# coding:utf-8
from appium import webdriver
import time
desired_caps = {}
desired_caps['appium-version'] = '1.0'
desired_caps['platformName'] = 'Android'
desired_caps['deviceName'] = 'e2109991'
desired_caps['appPackage'] = 'io.*****************.premium'
desired_caps['appActivity'] = '.ui.MainActivity'
driver = webdriver.Remote('http://0.0.0.0:4723/wd/hub', desired_caps)
def clickPermission():
    try:
        els = driver.find_elements_by_class_name('android.widget.Button')
        for el in els:
            if el.text == u'允许':
                driver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
            elif el.text == u'始终允许':
                driver.find_element_by_android_uiautomator('new UiSelector().text("始终允许")').click()
            elif el.text == u'确定':
                driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
    except:
        pass

def start():
    clickPermission()
    driver.find_element_by_id("channel_name").send_keys("111")
    driver.find_element_by_id("button_join").click()
    driver.find_element_by_id("button1").click()
    clickPermission()
    clickPermission()
    time.sleep(5)
    driver.quit()

if __name__ == '__main__':
    start()
