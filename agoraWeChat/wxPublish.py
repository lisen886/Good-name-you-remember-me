# python3
# -*- coding: UTF-8 -*-
import threading
import os
import subprocess
import base64

mp4cwd = os.getcwd()+"/wxPub.mp4"
# 为线程定义一个函数
def wx_publish(num):
    inputChannelName = "suilei" + str(num)
    print (inputChannelName)
    base64Name = (str(base64.b64encode(inputChannelName.encode('utf-8')), 'utf-8'))
    cmd ="ffmpeg -re -stream_loop -1 -i "+mp4cwd+" -c copy -f flv rtmp://test.mini-app.broadcastapp.agoraio.cn/live/" \
         "f4637604af81440596a54254d53ade20_"+base64Name+"_12345678"
    # 只推视频  -c copy -an -f flv
    # cmd ="ffmpeg -re -stream_loop -1 -i "+mp4cwd+" -c copy -an -f flv rtmp://test.mini-app.broadcastapp.agoraio.cn/live/" \
    #      "f4637604af81440596a54254d53ade20_"+base64Name+"_12345678"
    sub =subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    sub.wait()
    print (sub.stdout.read())

# 创建多线程
for i in range(1,11):
    threading.Thread(target=wx_publish, args=(i,)).start()