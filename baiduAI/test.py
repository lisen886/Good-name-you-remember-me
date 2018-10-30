# python2.7(Agora)
# -*- coding: UTF-8 -*-
import pyrec
import AipSpeechTest
import sys

class Test:
    def premiumTest(self):
        pyrec.rec("1.wav")
        pcm_file = AipSpeechTest.wav_to_pcm("1.wav")
        res_str = AipSpeechTest.audio_to_text(pcm_file)
        synthesis_file = AipSpeechTest.text_to_audio(res_str)
        AipSpeechTest.play_mp3(synthesis_file)

    def hiSiri(self):
        pyrec.rec("1.wav")
        pcm_file = AipSpeechTest.wav_to_pcm("1.wav")
        res_str = AipSpeechTest.audio_to_text(pcm_file)
        AipSpeechTest.open_application(res_str)

    def qaTest(self):
        pyrec.rec("1.wav")
        pcm_file = AipSpeechTest.wav_to_pcm("1.wav")
        q = AipSpeechTest.audio_to_text(pcm_file)
        ans = AipSpeechTest.qa(q)
        synthesis_file = AipSpeechTest.text_to_audio(ans)
        AipSpeechTest.play_mp3(synthesis_file)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('''run as: python test.py 1
                    1:premiumTest
                    2:hiSiri
                    3:qaTest''')
        exit(1)
    type = sys.argv[1]
    test = Test()
    if type == "1":
        test.premiumTest()
    elif type == "2":
        test.hiSiri()
    else:
        test.qaTest()
    AipSpeechTest.rmMp3()
