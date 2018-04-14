# python3
# -*- coding: UTF-8 -*-
import threading
import base64,re
from agoraWeChat.setup_ffprobe import FrameStat

# 为线程定义一个函数
def wx_Play(inputChannelName, uid):
    base64Name = (str(base64.b64encode(inputChannelName.encode('utf-8')), 'utf-8'))
    url = "rtmp://test.mini-app.broadcastapp.agoraio.cn/live/f4637604af81440596a54254d53ade20_"+base64Name+"_"+uid
    stat = FrameStat()
    stat.stat_frame(url, 100)
    audio = stat.audio_stat.get_stat_result()
    video = stat.video_stat.get_stat_result()
    if audio[1]>0 and video[1]>0:
        pass
    else:
        print(inputChannelName)
        # raise IOError

# # 创建多线程
threading.Thread(target=wx_Play, args=("suilei2",)).start()
threading.Thread(target=wx_Play, args=("suilei3",)).start()