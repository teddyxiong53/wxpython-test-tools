#coding: utf-8

from __future__ import print_function
import pyaudio
import wave
import threading

from logging import debug, error, info

from Config import *
import wave
import struct

READ_POS=20000

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
    def judgeSine(self, filename):
        result = ''
        self.inputWaveFile = wave.open(filename)
        if not self.inputWaveFile:
            result = '打开' + filename + "失败"
            return result
        print(self.inputWaveFile.getnframes())

        try:
            self.inputWaveFile.setpos(READ_POS)
        except:
            print("set pos fail")
            result = '文件'+ filename + '大小不对'
            return result
        data = self.inputWaveFile.readframes(16)
        # 取到数据后，需要大小端转换。
        # 得到的是一个元组。
        unpacked_data = struct.unpack("<16h", data)
        # print(unpacked_data)
        max_val = max(unpacked_data)
        min_val = min(unpacked_data)
        print(max_val)
        print(min_val)
        if max_val < SINE_ABS_BASE or abs(min_val) < SINE_ABS_BASE:
            result = '录音数据幅值太小'
            return result
        # 判断是否有截顶。
        for i in range(15):
            # print(i)
            if unpacked_data[i] == unpacked_data[i+1]:
                result = '有截顶'
                return result
        result = '正常'
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
        data = self.inputWaveFile.readframes(16000)
        # 取到数据后，需要大小端转换。
        # 得到的是一个元组。
        unpacked_data = struct.unpack("<16000h", data)
        # print(unpacked_data)
        max_val = max(unpacked_data)
        min_val = min(unpacked_data)
        print(max_val)
        print(min_val)
        if not (max_val < LINE_ABS_BASE and abs(min_val) < LINE_ABS_BASE):
            result = '降噪效果不好'
            return result
        return '正常'

if __name__ == '__main__':
    j = AudioJudge()
    j.judgeSine('input.wav')
