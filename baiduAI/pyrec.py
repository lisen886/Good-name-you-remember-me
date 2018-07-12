# python2.7(Agora)
# -*- coding: UTF-8 -*-
# brew install portaudio
# pip install pyaudio
import pyaudio
import wave
import AipSpeechTest

CHUNK = 1024  # 是一次读取的音频byte数量
FORMAT = pyaudio.paInt16  # 音频采样大小为16位
CHANNELS = 2  # 双声道
RATE = 16000  # 采样率
RECORD_SECONDS = 60  # 默认录制时间

def rec(file_name):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    try:
        AipSpeechTest.pt("开始录音,请说话 ...")
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        AipSpeechTest.pt("录音时间到 ...")
    except KeyboardInterrupt:
        AipSpeechTest.pt('强制录音结束 ...')

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
