#coding: utf-8

from __future__ import print_function
import pyaudio
import wave
import threading

from logging import debug, error, info

import Config

import wave
import struct
import math

READ_POS=20000

print = debug

left_y_data = []
right_y_data = []
ref_y_data = []
aec_y_data = []


class AudioJudge():
    '''
    判断逻辑：
    left、right、ref。
    这3个都是正弦波判断。
    1、取出一个周期的数据。
    2、判断最大值是否大于某个值。最小值是否小于某个值。这样是保证有数据。
    3、做截顶判断。就是判断是否有连续相等的2个点。
    seek到20000。读取32个字节数据。就是一个周期的数据。

    '''
    def judgeSine(self, filename, judgeValue):
        global left_y_data, right_y_data, ref_y_data
        print("比较基准值:{}".format(judgeValue))
        result = ''
        self.inputWaveFile = wave.open(filename)
        if not self.inputWaveFile:
            result = '打开' + filename + "失败"
            return result
        # print(self.inputWaveFile.getnframes())

        try:
            self.inputWaveFile.setpos(READ_POS)
        except:
            print("set pos fail")
            result = '录音文件大小不对'
            return result
        data = self.inputWaveFile.readframes(16)
        # 取到数据后，需要大小端转换。
        # 得到的是一个元组。
        unpacked_data = struct.unpack("<16h", data)
        if filename.find('left.wav') != -1:
            left_y_data = unpacked_data
        elif filename.find('right.wav') != -1:
            right_y_data = unpacked_data
        elif filename.find('ref.wav') != -1:
            ref_y_data = unpacked_data
        # 计算db值。
        # 算rms均方根值。
        db_val = 0
        for v in unpacked_data:
            print("v:{}".format(v))
            db_val += abs(v)*abs(v)
        print('sum:{}'.format(db_val))
        db_val = db_val/16
        # 然后开方
        db_val = math.sqrt(db_val)
        # 然后求对数。
        db_val = 20* math.log(db_val/32767,10)
        # 保留一位小数就好了
        db_val = round(db_val, 1)
        # print(unpacked_data)
        max_val = max(unpacked_data)
        min_val = min(unpacked_data)
        print("最大值：{}".format(max_val))
        print("最小值：{}".format(min_val))
        if max_val < judgeValue or abs(min_val) < judgeValue:
            result = '幅值太小({},{})'.format(min_val,max_val)
            if filename.find('ref.wav') != -1 and max_val<5:
                result += ',FL123问题'
            else:
                result += ',{}dB'.format(db_val)
            return result
        # 判断是否有截顶。
        for i in range(15):
            # print(i)
            if unpacked_data[i] == unpacked_data[i+1]:
                result = '有截顶'
                return result
        result = '正常'
        result += ',{}dB'.format(db_val)
        return result

    '''
    aec：
    这个就判断最大值小于某个值。希望尽量是一条直线。
    '''
    def judgeLine(self, filename):
        result = ''
        self.inputWaveFile = wave.open(filename)
        if not self.inputWaveFile:
            result = '打开' + filename + "失败"
            return result
        # print(self.inputWaveFile.getnframes())

        try:
            self.inputWaveFile.setpos(READ_POS)
        except:
            print("set pos fail")
            result = '文件'+ filename + '大小不对'
            return result
        data = self.inputWaveFile.readframes(160000) #除以16000，就是秒数。现在取10s。
        # 取到数据后，需要大小端转换。
        # 得到的是一个元组。
        unpacked_data = struct.unpack("<160000h", data)
        global aec_y_data
        aec_y_data = unpacked_data
        # print(unpacked_data)
        max_val = max(unpacked_data)
        min_val = min(unpacked_data)
        print("最大值：{}".format(max_val))
        print("最小值：{}".format(min_val))
        if not (max_val < Config.LINE_ABS_BASE and abs(min_val) < Config.LINE_ABS_BASE):
            result = '降噪不好({},{})'.format(min_val,max_val)
            return result
        return '正常'

if __name__ == '__main__':
    j = AudioJudge()
    j.judgeSine('input.wav')
