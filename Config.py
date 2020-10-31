#coding: utf-8

import pyaudio
import json

# 日志配置格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# 路径配置
AUDIO_OUTPUT_DIR='./audio_output'

LEFT_FILE=AUDIO_OUTPUT_DIR+'/left.wav'
RIGHT_FILE=AUDIO_OUTPUT_DIR+'/right.wav'
REF_FILE=AUDIO_OUTPUT_DIR+'/ref.wav'
AEC_FILE=AUDIO_OUTPUT_DIR+'/aec.wav'

MUSIC_FILE='music.wav'
INPUT_FILE="input.wav"

# 音频配置
CHUNK=1024
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=16000

# 结果判断
# 幅值的绝对值，不能小于这个值，否则说明信号太弱，或者就是直线。
SINE_ABS_BASE=10000
# AEC的判断，不能大于这个值，大于则说明降噪效果不好。
LINE_ABS_BASE=1000

def initConfig():
    global SINE_ABS_BASE, LINE_ABS_BASE
    with open('param.json') as f:
        param = json.load(f)
        # print(SINE_ABS_BASE)
        # print(param)
        SINE_ABS_BASE = param['SINE_ABS_BASE']
        LINE_ABS_BASE = param['LINE_ABS_BASE']
        # print(SINE_ABS_BASE)
if __name__ == '__main__':
    initConfig()
