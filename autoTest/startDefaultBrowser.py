import os,time
from selenium import webdriver

# ***************** Chrome读取配置文件允许摄像头权限 *****************
def startDefaultChromeByProfile():
    os.system("ps -ef | grep "+"Google"+" | grep -v grep | awk '{print $2}' | xargs kill -9")
    # os.system("cp ~/Desktop/chromedriver /usr/local/bin/")
    chrome_driver='/Users/lisen/Desktop/chromedriver'
    os.environ["webdriver.Chrome.driver"]=chrome_driver
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir=/Users/lisen/Library/Application Support/Google/Chrome")
    driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=option)
    driver.get("https://webdemo.agora.io/premium_rtc_test_2.5/show.html?channelName=asdsd&videoProfile=480p_4&uid=&uidtype=int&mode=live&codec=vp8&interop_mode=interop_commutication&avmode=0&dynamic=disabled&expiration=0&custom_key=&key=disabled&proxy=disabled&turnServerIP=113.207.108.198&udpPort=3478&tcpPort=3433&username=test&password=111111&forceTurn=disabled&nginxURL=webopt.agorabeckon.com&encrypt=disabled&encryptMode=none&encryptPassword=&preprocessing=disabled")
    time.sleep(5)
    print(driver.capabilities['version'])
    driver.quit()


# ***************** Firefox读取配置文件允许摄像头权限 *****************
def startDefaultFirefoxByProfile():
    firefox_driver='/Users/lisen/Desktop/geckodriver57+'
    MacFirefoxPath="/Users/lisen/Library/Application Support/Firefox/Profiles/28mwdrcp.default"
    os.environ["webdriver.Firefox.driver"]=firefox_driver
    firefoxProfile = webdriver.FirefoxProfile(MacFirefoxPath)
    driver = webdriver.Firefox(executable_path=firefox_driver,firefox_profile=firefoxProfile)
    driver.get("https://webdemo.agora.io/premium_rtc_test_2.5/show.html?channelName=asdsd&videoProfile=480p_4&uid=&uidtype=int&mode=live&codec=vp8&interop_mode=interop_commutication&avmode=0&dynamic=disabled&expiration=0&custom_key=&key=disabled&proxy=disabled&turnServerIP=113.207.108.198&udpPort=3478&tcpPort=3433&username=test&password=111111&forceTurn=disabled&nginxURL=webopt.agorabeckon.com&encrypt=disabled&encryptMode=none&encryptPassword=&preprocessing=disabled")
    time.sleep(5)
    driver.quit()


# **************   Chrome不需要读默认文件的允许摄像头权限   ************** #
def startChromeBySetOption():
    chrome_driver='/Users/lisen/Desktop/chromedriver'
    os.environ["webdriver.Chrome.driver"]=chrome_driver
    option = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values.media_stream_camera': 1,
             'profile.default_content_setting_values.media_stream_mic': 1,
             'profile.default_content_setting_values.notifications': 1,
             'profile.default_content_setting_values.geolocation': 1}
    option.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=option)
    driver.get("https://webdemo.agora.io/premium_rtc_test_2.5/show.html?channelName=asdsd&videoProfile=480p_4&uid=&uidtype=int&mode=live&codec=vp8&interop_mode=interop_commutication&avmode=0&dynamic=disabled&expiration=0&custom_key=&key=disabled&proxy=disabled&turnServerIP=113.207.108.198&udpPort=3478&tcpPort=3433&username=test&password=111111&forceTurn=disabled&nginxURL=webopt.agorabeckon.com&encrypt=disabled&encryptMode=none&encryptPassword=&preprocessing=disabled")
    time.sleep(5)
    print(driver.capabilities['version'])
    driver.quit()

# **************   Firefox不需要读默认文件的允许摄像头权限   ************** #
def startFirefoxBySetOption():
    firefox_driver='/Users/lisen/Desktop/geckodriver63'
    os.environ["webdriver.Firefox.driver"]=firefox_driver
    profile = webdriver.FirefoxProfile()
    profile.set_preference ('media.navigator.permission.disabled', True)
    profile.update_preferences()
    driver = webdriver.Firefox(executable_path=firefox_driver,firefox_profile=profile)
    driver.get("https://webdemo.agora.io/premium_rtc_test_2.5/show.html?channelName=asdsd&videoProfile=480p_4&uid=&uidtype=int&mode=live&codec=vp8&interop_mode=interop_commutication&avmode=0&dynamic=disabled&expiration=0&custom_key=&key=disabled&proxy=disabled&turnServerIP=113.207.108.198&udpPort=3478&tcpPort=3433&username=test&password=111111&forceTurn=disabled&nginxURL=webopt.agorabeckon.com&encrypt=disabled&encryptMode=none&encryptPassword=&preprocessing=disabled")
    time.sleep(5)
    driver.quit()

