#coding: utf-8

import pyaudio
import json
# 版本号
SOFTWARE_VERSION = "V2.2"
SOFTWARE_NAME = "DOSS会议音箱测试软件"
SOFTWARE_AUTHOR = "熊汉良"

# 日志配置格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# 路径配置
AUDIO_OUTPUT_DIR='./audio_output'

LEFT_FILE=AUDIO_OUTPUT_DIR+'/left.wav'
LEFT_FILE_100HZ=AUDIO_OUTPUT_DIR+'/left_100hz.wav'
LEFT_FILE_300HZ=AUDIO_OUTPUT_DIR+'/left_300hz.wav'

RIGHT_FILE=AUDIO_OUTPUT_DIR+'/right.wav'
RIGHT_FILE_100HZ=AUDIO_OUTPUT_DIR+'/right_100hz.wav'
RIGHT_FILE_300HZ=AUDIO_OUTPUT_DIR+'/right_300hz.wav'

REF_FILE=AUDIO_OUTPUT_DIR+'/ref.wav'
AEC_FILE=AUDIO_OUTPUT_DIR+'/aec.wav'

MUSIC_FILE='music.wav'
INPUT_FILE="input.wav"
INPUT_FILE_100HZ="100hz.wav"
INPUT_FILE_300HZ="300hz.wav"

# 音频配置
CHUNK=1024
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=16000

# 结果判断
# 幅值的绝对值，不能小于这个值，否则说明信号太弱，或者就是直线。
SINE_ABS_BASE=-29.8
SINE_ABS_BASE_100HZ=-29.8
SINE_ABS_BASE_300HZ=-29.8

# ref的单独配置
REF_SINE_ABS_BASE=10000

# AEC的判断，不能大于这个值，大于则说明降噪效果不好。
LINE_ABS_BASE=1000
# 大于LINE_ABS_BASE的点累积超过这个数，才认为不合格。
LINE_POINTS=1000

PCBA = False
WAV_100HZ = False
WAV_300HZ = False

def initConfig():
    global SINE_ABS_BASE, LINE_ABS_BASE,REF_SINE_ABS_BASE, PCBA, WAV_100HZ, WAV_300HZ,LINE_POINTS,SINE_ABS_BASE_100HZ,SINE_ABS_BASE_300HZ
    with open('config/param.json') as f:
        param = json.load(f)
        # print(SINE_ABS_BASE)
        # print(param)

        PCBA = param['PCBA']
        print('pcba value:', PCBA)
        WAV_100HZ = param['WAV_100HZ']
        WAV_300HZ = param['WAV_300HZ']
        LINE_POINTS = param['LINE_POINTS']


        SINE_ABS_BASE = param['SINE_ABS_BASE']
        SINE_ABS_BASE_100HZ = param['SINE_ABS_BASE_100HZ']
        SINE_ABS_BASE_300HZ = param['SINE_ABS_BASE_300HZ']

        REF_SINE_ABS_BASE = param['REF_SINE_ABS_BASE']


        if param['LINE_ABS_BASE'] and 0 <= param['LINE_ABS_BASE'] <= 40000:
            LINE_ABS_BASE = param['LINE_ABS_BASE']
        else:
            print("LINE_ABS_BASE invalid:", param['LINE_ABS_BASE'])

if __name__ == '__main__':
    initConfig()
