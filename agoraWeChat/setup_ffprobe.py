import json
import subprocess
# by sh hero

FFPROBE_FRAMES = 'ffprobe -of json -v quiet -show_frames -i %s'
FFPROBE_STREAMS = 'ffprobe -of json -v quiet -show_streams -i %s'


class AudioStat:
    def __init__(self):
        self.bitrate = []
        self.calc_bitrate = 0
        self.calc_samplerate = 0.0
        self.last_dts = 0.0

        self.channels = None
        self.profile = None
        self.samplerate = None
        self.stream_bitrate = None

    def get_stat_result(self):
        if self.stream_bitrate is None and len(self.bitrate) == 0:
            print('audio error too few frames')
            return '', 0, 0, 0

        bps = round(sum(self.bitrate) / len(self.bitrate), 2) if self.stream_bitrate is None else self.stream_bitrate
        print('audio profile:', self.profile, 'bitrate:', bps, 'bps samplerate:',
              self.samplerate, 'channels:', self.channels)
        return self.profile, bps, self.samplerate, self.channels

    def parse_stream(self, frame):
        if self.channels is None and 'channels' in frame:
            self.channels = int(frame['channels'])

        if self.profile is None and 'profile' in frame:
            self.profile = frame['profile']

        if self.samplerate is None and 'sample_rate' in frame:
            self.samplerate = int(frame['sample_rate'])

        if self.stream_bitrate is None and 'bit_rate' in frame:
            self.stream_bitrate = int(frame['bit_rate']) / 1000

    def parse_frame(self, frame):
        if frame['media_type'] != 'audio':
            return

        if self.channels is None and 'channels' in frame:
            self.channels = int(frame['channels'])

        if self.samplerate is None and 'pkt_duration' in frame:
            duration = int(frame['pkt_duration'])
            if duration == 21:
                self.samplerate = 48000
            if duration == 23:
                self.samplerate = 44100
            if duration == 32:
                self.samplerate = 32000

        now_dts = float(frame['pkt_pts_time'])
        if self.last_dts == 0:
            self.last_dts = now_dts

        if now_dts - self.last_dts > 1:
            self.bitrate.append(self.calc_bitrate * 8 / (now_dts - self.last_dts))
            self.calc_bitrate = 0

            self.last_dts = now_dts

        if 'pkt_size' in frame:
            self.calc_bitrate += int(frame['pkt_size'])


class VideoStat:
    def __init__(self):
        self.gop = []
        self.bitrate = []
        self.framerate = []
        self.calc_gop = 0
        self.calc_bitrate = 0
        self.calc_framerate = 0
        self.last_dts = 0.0

        self.profile = None
        self.resolution = None
        self.stream_framerate = None

    def get_stat_result(self):
        if len(self.bitrate) == 0 or len(self.framerate) == 0 or len(self.gop) == 0:
            print('video error too few frames')
            return '', 0, 0, 0, (0, 0)

        bps = round(sum(self.bitrate) / len(self.bitrate), 2)
        # donot use fps calc from ffprobe stream stat, there's some problem in 3.3.3
        # fps = int(sum(self.framerate) / len(self.framerate)) if self.stream_framerate is None else self.stream_framerate
        fps = int(sum(self.framerate) / len(self.framerate))
        group_pic_cnt = int(sum(self.gop) / len(self.gop))
        print('video profile:', self.profile, 'bitrate', bps, 'bps framerate:', fps,
              'gop:', group_pic_cnt, 'resolution:', self.resolution)
        return self.profile, bps, fps, group_pic_cnt, self.resolution

    def parse_stream(self, frame):
        if self.profile is None and 'profile' in frame:
            self.profile = frame['profile']

        if self.resolution is None and 'width' in frame and 'height' in frame:
            self.resolution = (int(frame['width']), int(frame['height']))

        if self.stream_framerate is None and 'avg_frame_rate' in frame:
            self.stream_framerate = eval(frame['avg_frame_rate'])

    def parse_frame(self, frame):
        if frame['media_type'] != 'video':
            return

        if self.resolution is None and 'width' in frame and 'height' in frame:
            self.resolution = (int(frame['width']), int(frame['height']))

        if 'key_frame' in frame and frame['key_frame'] == 1 and self.calc_gop != 0:
            self.gop.append(self.calc_gop)
            self.calc_gop = 0
        self.calc_gop += 1

        if 'pkt_pts_time' not in frame:
            return

        now_dts = float(frame['pkt_pts_time'])
        if self.last_dts == 0:
            self.last_dts = now_dts

        if now_dts - self.last_dts > 1:
            self.framerate.append(self.calc_framerate / (now_dts - self.last_dts))
            self.calc_framerate = 0

            self.bitrate.append(self.calc_bitrate * 8 / (now_dts - self.last_dts))
            self.calc_bitrate = 0

            self.last_dts = now_dts
        self.calc_framerate += 1

        if 'pkt_size' in frame:
            self.calc_bitrate += int(frame['pkt_size'])


class FrameStat:
    def __init__(self):
        self.subp = None
        self.audio_stat = AudioStat()
        self.video_stat = VideoStat()

    def stat_frame(self, url, stat_frame_count):
        for frame_json in self.run_ffprobe_streams(url):
            frame = json.loads(frame_json)

            if 'codec_type' not in frame:
                continue

            frame_type = frame['codec_type']
            if frame_type == 'audio':
                self.audio_stat.parse_stream(frame)
                continue

            if frame_type == 'video':
                self.video_stat.parse_stream(frame)
                continue

        if self.subp is not None:
            try:
                self.subp.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.subp.terminate()
            self.subp = None

        audio_frame_count = 0
        video_frame_count = 0
        for frame_json in self.run_ffprobe_frames(url):
            frame = json.loads(frame_json)

            if 'media_type' not in frame:
                continue

            frame_type = frame['media_type']
            if audio_frame_count < stat_frame_count and frame_type == 'audio':
                self.audio_stat.parse_frame(frame)
                audio_frame_count += 1
                continue

            if video_frame_count < stat_frame_count and frame_type == 'video':
                self.video_stat.parse_frame(frame)
                video_frame_count += 1
                continue

            if audio_frame_count == stat_frame_count and video_frame_count == stat_frame_count:
                break

        if self.subp is not None:
            try:
                self.subp.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.subp.terminate()
            self.subp = None

    def run_ffprobe_streams(self, url):
        self.subp = subprocess.Popen(FFPROBE_STREAMS % url, stdout=subprocess.PIPE, shell=True)
        frame = ''
        is_start = False
        while True:
            out = self.subp.stdout.readline().decode().strip()
            if out == '' and self.subp.poll() is not None:
                break

            if not is_start:
                if out == '{':
                    continue
                if out == '"streams": [':
                    is_start = True
                    continue

            if out == '{':
                frame = out
                continue

            if out == '},' or out == '}':
                if len(frame) == 0:
                    continue

                frame += out[0]
                frame += '}'
                yield frame
                frame = ''

            if len(frame) != 0:
                frame += out

    def run_ffprobe_frames(self, url):
        self.subp = subprocess.Popen(FFPROBE_FRAMES % url, stdout=subprocess.PIPE, shell=True)
        frame = ''
        is_start = False
        while True:
            out = self.subp.stdout.readline().decode().strip()
            if out == '' and self.subp.poll() is not None:
                print('cannot pull stream for frames, please check the url')
                break

            if not is_start:
                if out == '{':
                    continue
                if out == '"frames": [':
                    is_start = True
                    continue

            if out == '{':
                frame = out
                continue

            if out == '},':
                frame += out[0]
                yield frame

            frame += out


# if __name__ == '__main__':
#     import sys
#     if len(sys.argv) < 2:
#         print('run as: python3 setup_ffprobe.py rtmp://xxxx')
#         exit(1)
#     url = sys.argv[1]
#     stat = FrameStat()
#     try:
#         stat.stat_frame(url, 100)
#         stat.audio_stat.get_stat_result()
#         stat.video_stat.get_stat_result()
#     except KeyboardInterrupt as e:
#         print('Stop ...')
