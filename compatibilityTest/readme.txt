使用说明：
1、将isntallDemo中的browserConfig.json和installApplication_interface.py拷贝到compatibility目录下
2、compatibility目录下新建chrome和firefox文件夹，存放浏览器安装包
3、执行browserCompatibility.py(windows chrome 卸载的确定按钮可通过pyautogui enter)

* https://github.com/mozilla/geckodriver/releases
* https://blog.csdn.net/huilan_same/article/details/51896672?locationNum=11&fps=1

目录结构如下

-compatibilitTest
    -chrome
       .chromewindows_59_installer.exe(名字需要在browserConfig.json和版本对应)
       .chromemac59.dmg
    -firefox
       .firefoxwindows_59_installer.exe
       .firefoxmac59.dmg
    -webdriver
        -mac
            -chrome
                .chromedriver2.21
                .chromedriver2.22
            -firefox
                .geckodriver55+
                .geckodriver57+
        -windows
            -chrome
                .chromedriver2.21.exe
                .chromedriver2.22.exe
            -firefox
                .geckodriver55+.exe
                .geckodriver57+.exe
    .browserConfig.json
    .installApplication_interface.py
    .browserCompatibility.py
    .webdriverMap.json
