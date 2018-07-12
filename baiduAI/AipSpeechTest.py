# python2.7(Agora)
# -*- coding: UTF-8 -*-
from aip import AipSpeech
import os
APP_ID = '11508980'
API_KEY = '8bt65fVa9LBbFwoXfpaKqKIS'
SECRET_KEY = 'yMyxPqY2KCBWV5px0jO6N8lIUyyalf4s'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# https://cloud.baidu.com/doc/SPEECH/ASR-Online-Python-SDK.html#.E6.8E.A5.E5.8F.A3.E8.AF.B4.E6.98.8E
def audio_to_text(pcm_file):
    with open(pcm_file, 'rb') as fp:
        file_context = fp.read()
    # 调用百度AI的语音识别接口
    res = client.asr(file_context, 'pcm', 16000, {
        'dev_pid': 1536,  # 普通话(支持简单的英文识别)
    })
    # 获取返回值字典中的结果
    res_str = res.get("result")[0]
    pt(res_str)
    return res_str

# https://cloud.baidu.com/doc/SPEECH/TTS-Online-Python-SDK.html#.E6.8E.A5.E5.8F.A3.E8.AF.B4.E6.98.8E
def text_to_audio(res_str):
    synthesis_file = "synthesis.mp3"
    # 调用百度AI的语音合成接口
    synthesis_context = client.synthesis(res_str, "zh", 1, {
        "vol": 6,  # 音量 0~15
        "spd": 4,  # 语速 0~15
        "pit": 3,  # 音调 0~15
        "per": 0   # 变声 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫
    })
    if not isinstance(synthesis_context, dict):
        with open('synthesis.mp3', 'wb') as f:
            f.write(synthesis_context)
    return synthesis_file

def play_mp3(file_name):
    os.system("ffplay -autoexit %s"%(file_name))

def wav_to_pcm(wav_file):
    pcm_file = "%s.pcm" % (wav_file.split(".")[0])
    # https://blog.csdn.net/cinberella/article/details/43833189 ffmpeg命令：wav转pcm,pcm转wav
    os.system("ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s" % (wav_file, pcm_file))
    return pcm_file

def open_application(res_str):
    if "Firefox" in res_str or u"火狐" in res_str:
        print("open firefox")
        os.system("open /Applications/firefox.app")
    elif "QQ" in res_str or "qq" in res_str:
        print("open QQ")
        os.system("open /Applications/QQ.app")
    elif u"微信" in res_str:
        print("open WeChat")
        os.system("open /Applications/WeChat.app")
    else:
        ans = "我不知道你在说啥"
        ansAudio= text_to_audio(ans)
        play_mp3(ansAudio)

def pt(message):
    print('\033[1;31;40m')
    print('*' * 50)
    print(message)
    print('*' * 50)
    print('\033[0m')

def rmMp3():
    try:
        os.system("rm *.pcm")
        os.system("rm *.wav")
        os.system("rm *.mp3")
    except:
        pass

def qa(res_str):
    if u"名字" in res_str:
        a = "我叫皮皮虾"
    else:
        a = "我还小，不会说话"
    return a
