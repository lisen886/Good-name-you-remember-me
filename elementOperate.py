# -*- coding: utf-8 -*-
import time,os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from case.toolLib.result import Result
from case.caseLib.configure.basicMethod import BasicMethod
from selenium.webdriver.support.select import Select
from lib.runnerHelper import RunnerHelper
class ElementOperate:
    caseLog = Result()
    screenShotName = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()) + ".png"
    def __init__(self,driver):
        self.driver = driver
    """
    summary: 通过指定定位器来寻找元素
    return: element
    author: lisen sui
    """
    def __findElement (self, selector, value):
        if selector == "id":
            element = self.driver.find_element_by_id(value)
        elif selector == "name":
            element = self.driver.find_element_by_name(value)
        elif selector == "class_name":
            element = self.driver.find_element_by_class_name(value)
        elif selector == "link_text":
            element = self.driver.find_element_by_link_text(value)
        elif selector == "partial_link_text":
            element = self.driver.find_element_by_partial_link_text(value)
        elif selector == "tag_name":
            element = self.driver.find_element_by_tag_name(value)
        elif selector == "xpath":
            element = self.driver.find_element_by_xpath(value)
        elif selector == "css":
            element = self.driver.find_element_by_css_selector(value)
        elif selector == "iosid":
            element = self.driver.find_element_by_accessibility_id(value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")
        return element
    """
    summary: 通过指定定位器来寻找元素集合
    return: elements
    author: lisen sui
    """
    def __findElements(self,selector,value):
        if selector == "id":
            elements = self.driver.find_elements_by_id(value)
        elif selector == "name":
            elements = self.driver.find_elements_by_name(value)
        elif selector == "class_name":
            elements = self.driver.find_elements_by_class_name(value)
        elif selector == "link_text":
            elements = self.driver.find_elements_by_link_text(value)
        elif selector == "partial_link_text":
            elements = self.driver.find_elements_by_partial_link_text(value)
        elif selector == "tag_name":
            elements = self.driver.find_elements_by_tag_name(value)
        elif selector == "xpath":
            elements = self.driver.find_elements_by_xpath(value)
        elif selector == "css":
            elements = self.driver.find_elements_by_css_selector(value)
        elif selector == "ios":
            elements = self.driver.find_element_by_accessibility_id(value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")
        return elements

    def findElementById(self, value):
        return self.driver.find_element_by_id(value)

    """
    summary: 通过判断找元素，存在返回，不存在就等待
    return: element
    author: lisen sui
    """
    def findMyElement(self,by,value):
        #判断元素是否存在，存在就返回元素
        if(self.__isElementExist(by,value)):
            # self.caseLog.log("找到元素"+ value)
            element=self.__findElement(by,value)
            return element
        #不存在开启显性等待
        else:
            try:
                waitFindElement=self.obviousWait(by,value)
                return waitFindElement
                #依旧不存在就处理异常
            except:
                self.caseLog.log("元素不存在，或者超过设定时间未找到")
                self.screenShot()
                return None

    def findMyElementNotShot(self,by,value):
        if(self.__isElementExist(by,value)):
            # self.caseLog.log("找到元素"+ value)
            element=self.__findElement(by,value)
            return element
        else:
            try:
                waitFindElement=self.obviousWait(by,value)
                return waitFindElement
            except:
                self.caseLog.log("元素不存在，或者超过设定时间未找到")
                return None
    """
    summary: 通过判断找元素集合，存在返回，不存在开启显性等待
    return:
    author: lisen sui
    """
    def findMyElements(self,by,value):
        if (self.__isElementExist(by, value)):
            self.caseLog.log("找到元素集合" + value)
            elements = self.__findElements(by, value)
            return elements
        else:
            try:
                self.obviousWait(by, value)
                waitFindElements=self.__findElements(by,value)
                return waitFindElements
            except:
                self.caseLog.log("元素不存在，或者超过设定时间未找到")
                self.screenShot()
                return None
    """
    summary: 封装元素click
    return:
    author: lisen sui
    """
    def clickElement(self,by,value):
        self.findMyElement(by,value).click()
        self.caseLog.log("点击元素：%s" % value)
    """
    summary: 勾选单选框、复选框
    return:
    author: lisen sui
    """
    def hookElement(self,by,value):
        element = self.findMyElement(by,value)
        attribute = element.get_attribute("checked")
        if attribute == "true":
            pass
        else:
            element.click()
        self.caseLog.log("勾选元素：%s" % value)
    def removeHookElement(self,by,value):
        element = self.findMyElement(by, value)
        attribute = element.get_attribute("checked")
        if attribute == "true":
            element.click()
        else:
            pass
        self.caseLog.log("去掉勾选：%s" % value)
    """
    summary: 封装元素clear
    return:
    author: lisen sui
    """
    def clearText(self,by,value):
        self.findMyElement(by,value).clear()
        self.caseLog.log("清空元素：%s" % value)
    """
    summary: appium sendKey
    return:
    author: lisen sui
    """
    def clearAndSendkey(self,by,value,text):
        self.clearText(by,value)
        # self.findMyElement(by,value).send_keys(text)
        self.findMyElement(by,value).set_value(text)
        self.caseLog.log("输入：%s" % text)
        #ios需要退出键盘
        self.hide_keyboard()
    """
    summary: selenium sendkey
    return:
    author: lisen sui
    """
    def sendKeyWeb(self,by,value,text):
        self.clearText(by, value)
        self.findMyElement(by,value).send_keys(text)
        self.caseLog.log("输入：%s" % text)
    """
    summary: 获取文本信息
    return:
    author: lisen sui
    """
    def getText(self,by,value):
        return self.findMyElement(by,value).text
    """
    summary: 这是一个判断元素是否存在的方法
    return:
    author: lisen sui
    """
    def __isElementExist(self,by,value):
        try:
            self.__findElement(by,value)
            return True
        except:
            return False
    """
    summary: 显性等待，设置10s，当3s时找到元素就执行下一步
    return: WebElement
    author: lisen sui
    """
    def obviousWait(self,by,value):
        self.caseLog.log("%s 元素没找到，开启显性等待!,5s内还没找到报错退出!"%value)
        if by == "id":
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, value)))
        elif by == "name":
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, value)))
        elif by == "xpath":
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, value)))
        elif by == "class_name":
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        else:
            raise NameError("Please enter a valid type of targeting elements.")
        self.caseLog.log("等待后找到元素%s"%value)
        return element

    """
    通过is_displayed()实现显性等待
    """
    def waitForMe(self,by,value):
        for i in range(5):
            element=self.__findElement(by,value)
            if element.is_displayed():
                return element
    """
    summary: 强制等待
    return:
    author: lisen sui
    """
    def sleep(self,seconds):
        self.caseLog.log("开启强制等待%s秒钟"%seconds)
        time.sleep(seconds)
    """
    summary: 隐形等待
    return:
    author: lisen sui
    """
    def invisibleWait(self,seconds):
        self.caseLog.log("开启隐形等待%s秒钟" % seconds)
        self.driver.implicitly_wait(seconds)
    """
    summary: 封装select，by value/by text
    return:
    author: lisen sui
    """
    def selectByValue(self,by,byValue,value):
        element = self.findMyElement(by,byValue)
        Select(element).select_by_value(value)

    def selectByText(self,by,byValue,text):
        element = self.findMyElement(by, byValue)
        Select(element).select_by_visible_text(text)

    def selectByIndex(self,by,byValue,index):
        element = self.findMyElement(by, byValue)
        Select(element).select_by_index(index)
    """
    summary: 失败截图
    return:
    author: lisen sui
    """
    def screenShot(self):
        # currentPath = os.path.abspath('.')
        # screenPath = currentPath + "/screenShot"
        # if not os.path.exists(screenPath):
        #     os.makedirs(screenPath)
        screenPath = RunnerHelper().getLogPath()
        png = self.driver.get_screenshot_as_png()
        with open(screenPath+'/'+self.screenShotName, 'wb') as f:
            f.write(png)
            self.caseLog.log("保存图片：" + self.screenShotName)

    """
    summary: 系统弹窗,权限允许,通过adb点击坐标的方式解决
    return:
    author: lisen sui
    """
    def permission(self):
        os.system("adb shell input tap " + str(0) + " " + str(1645))

    def click_shoot_windows(self):
        try:
            els = self.driver.find_elements_by_class_name('android.widget.Button')
            for el in els:
                if el.text == u'允许':
                    self.driver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
                elif el.text == u'始终允许':
                    self.driver.find_element_by_android_uiautomator('new UiSelector().text("始终允许")').click()
                elif el.text == u'确定':
                    self.driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
        except:
            pass
    """
    summary: 切换窗口
    return:
    author: lisen sui
    """
    def switchAlert(self):
        self.driver.switch_to_alert()
    """
    summary:
    return: 收起ios键盘
    author: lisen sui
    """
    def hide_keyboard(self):
        self.driver.hide_keyboard("Return")
        # self.driver.tap([(20, 20)])
    """
     summary: 检查点，a，b相等，pass，不相等，AssertError
     return:
     author: lisen sui
     """

    def checkPoint(self, a, b):
        assert a == b, 'check point error'
    """
    summary: 获取属性值
    return:
    author: lisen sui
    """
    def getAttributeValue(self,by, value):
        element = self.findMyElement(by, value)
        attribute = element.get_attribute("checked")
        if attribute == "true":
            return attribute
        else:
            element.click()
            return attribute
    """
    summary: 滑动屏幕（element1-->element2）
    return:
    author: lisen sui
    """
    def scrollScreen(self,by1, value1, by2, value2):
        self.driver.scroll(self.findMyElement(by1,value1), self.findMyElement(by2,value2))





