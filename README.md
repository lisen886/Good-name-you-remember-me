## test_tool
### 一、环境搭建
#### 1. [Mac上搭建python+appium](http://www.cnblogs.com/tangdongchu/p/4432808.html)
#### 2. [Windows上搭建python+appium](https://testerhome.com/topics/646)
### 二、工具介绍
#### 1. [python 的设计模式](http://www.cnblogs.com/wuyuegb2312/archive/2013/04/09/3008320.html)本工具使用的是简单工厂模式以及建造者模式
#### 2. 框架介绍
(1) 工具调用：case-->toolLib-->lib

(2) androidCase调用androidLib调用pageLevel调用元素操作类(elementOperate.py)

* pageLevel层编写底层功能点操作方法
* androidLib层编写接口逻辑操作方法
* androidCase层编写测试用例操作方法

(3) iosCase

(4) macChromeCase
### 三、编码规则
 1. 尽量使用完整的英文描述符
 2. 类名，使用完整的英文描述符，首字母大写，使用驼峰命名法，例如: class JoinCommunicateChannel()
 3. 普通成员方法，采用完整英文描述符说明成员方法功能，首字母小写，例如：def clickJoinButton()
 4. python文件名采用完整英文描述符说明成员方法功能，首字母小写，例如：startPremium.py
 5. case文件名使用与TestLink相对应的ID，例如：Live-718.py
 6. 注释，包括：类或方法的目的，返回值
### 四、服务启动
 1.appium
   * appium -a 0.0.0.0 -p 4723 --session-override
   * appium -a 0.0.0.0 -p 4725 --session-override
   
 2.selenium
   * java -jar (selenium-server-standalone-2.45.0.jar路径) -role hub
   * java -jar (selenium-server-standalone-2.45.0.jar路径) -hub http://localhost:4444/grid/register -browser "browserName=chrome,version=（chrome version）,platform=MAC" -role webdriver
### 五、注意
 * __如果你看见`IOError: [Errno 2] No such file or directory: '/Users/lisen/Desktop/Agora_runner/configure.xml' `请运行run.py去执行脚本__
 * Move chromedriver to system property: sudo cp chromedriver /usr/local/bin
### 六、code
#### 元素操作类(elementOperate.py)
 1. def __findElement(self, selector, value)封装appium单个元素定位方式的私有接口
   * selector:选择器；可以选择id、name、class_name、xpath等定位方式
   * value:定位元素的属性值
 2. def __findElements(self, selector, value)封装appium元素集合定位方式的私有接口
   * selector:选择器；可以选择id、name、class_name、xpath等定位方式
   * value:定位元素的属性值
 3. def findMyElement(self,by,value) 封装寻找元素的接口
 ```
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
 ```
 4. def clickElement(self,by,value)封装点击元素接口
 5. def hookElement(self,by,value)封装勾选元素接口
 ```
     def hookElement(self,by,value):
        element = self.findMyElement(by,value)
        attribute = element.get_attribute("checked")
        #判断元素是否已经被勾选
        if attribute == "true":
            pass
        else:
            element.click()
        self.caseLog.log("勾选元素：%s" % value)
 ```
 6. def clearText(self,by,value)封装清除文本操作
 7. def clearAndSendkey(self,by,value,text) 清除并输入操作
 ```
     def clearAndSendkey(self,by,value,text):
        self.clearText(by,value)
        # selenium 3.0后使用set_value来输入文本
        self.findMyElement(by,value).set_value(text)
        self.caseLog.log("输入：%s" % text)
        #ios需要退出键盘
        self.hide_keyboard()
 ```
 8. def sendKeyWeb(self,by,value,text)封装web输入操作(web还是使用send_keys)
 9. def getText(self,by,value)获取文本操作
 10. def __isElementExist(self,by,value)判断元素是否存在
 11. def obviousWait(self,by,value)显性等待，设置10s，当3s时找到元素就执行下一步
 ```
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
 ```
 12. def selectByValue(self,by,byValue,value)封装select操作
 13. def screenShot(self)截图
 ```
     def screenShot(self):
        screenPath = RunnerHelper().getLogPath()
        png = self.driver.get_screenshot_as_png()
        with open(screenPath+'/'+self.screenShotName, 'wb') as f:
            f.write(png)
            self.caseLog.log("保存图片：" + self.screenShotName)
 ```
 14. def click_shoot_windows(self)系统弹窗,权限允许,通过adb点击坐标的方式解决
 ```
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
 ```
 15. def hide_keyboard(self)收起ios键盘
 16. def scrollScreen(self,by1, value1, by2, value2)滑动屏幕（element1-->element2）
 17. def checkPoint(self, a, b)封装检查点
 ```
      def checkPoint(self, a, b):
        assert a == b, 'check point error'
 ```
 