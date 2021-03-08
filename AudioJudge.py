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

# print = debug

left_y_data = []
right_y_data = []
ref_y_data = []
aec_y_data = []

def calc_db(data, points):
    db_val = 0

    for v in data:
        db_val += abs(v)*abs(v)
    # print('sum:{}'.format(db_val))
    db_val = db_val/points
    # 然后开方
    db_val = math.sqrt(db_val)
    # 然后求对数。
    db_val = 20* math.log(db_val/32767,10)
    # 保留一位小数就好了
    db_val = round(db_val, 1)
    return db_val

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
    def judgeSine(self, filename, judgeValue, rate):
        global left_y_data, right_y_data, ref_y_data
        print("比较基准值:{}".format(judgeValue))
        result = ''
        self.inputWaveFile = wave.open(filename)
        if not self.inputWaveFile:
            result = '打开' + filename + "失败"
            return result
        # print(self.inputWaveFile.getnframes())
        read_pos = READ_POS
        read_size = 16
        if filename.find('100hz.wav') != -1:
            read_pos = READ_POS
            read_size = 160
        elif filename.find('300hz.wav') != -1:
            read_pos = READ_POS
            read_size = 54 # 保证至少有一个完整的正弦波。
        try:
            self.inputWaveFile.setpos(read_pos)
        except:
            print("set pos fail")
            result = '录音文件大小不对'
            return result
        data = self.inputWaveFile.readframes(read_size)
        # 取到数据后，需要大小端转换。
        # 得到的是一个元组。
        parse_fmt = '<{}h'.format(read_size)
        unpacked_data = struct.unpack(parse_fmt, data)
        # print('----------------{}'.format(filename))
        # print(unpacked_data)
        # 对于100hz和300hz的，只看最大值和最小值。
        if filename.find('00hz.wav') != -1:
            # 现在因为设置值是dB值，所以还是需要计算dB值来比较。
            db_val = calc_db(unpacked_data, read_size)
            print('{}文件的db计算结果为：{}'.format(filename, db_val))
            if db_val < judgeValue:
                result = '幅值太小({}dB)'.format(db_val)
                return result
            # 判断是否有截顶。
            for i in range(read_size-1):
                # print(i)
                if unpacked_data[i] == unpacked_data[i+1] and unpacked_data[i]>=32767:
                    #print('{}:{},{}:{}'.format(i, unpacked_data[i], i+1, unpacked_data[i+1]))
                    result = '有截顶'
                    return result
            return '正常,{}dB'.format(db_val)

        if filename.find('left.wav') != -1:
            left_y_data = unpacked_data
        elif filename.find('right.wav') != -1:
            right_y_data = unpacked_data
        elif filename.find('ref.wav') != -1:
            ref_y_data = unpacked_data
        # 先判断波形是否符合正弦波规律，不符合，就直接返回，后面的判断也就不用做了。
        sign_change_times = 0 # 数值符号改变的次数，一个完整正常的正弦波，符号只变化两次。多了少了，多说明波形不是正常的正弦波。
        # 实测发现，变化一次的也是正常的。
        for i in range(15):
            a = unpacked_data[i]
            b = unpacked_data[i+1]
            # print('{}:{}'.format(a,b))
            if a == 0 or b==0:
                print("some value is zero:a:{},b:{}".format(a,b))
            if a*b < 0:
                sign_change_times += 1
        if not (sign_change_times == 2 or sign_change_times == 1):
            result = "波形畸变，有问题：{}".format(sign_change_times)
            return result

        # 计算db值。
        # 算rms均方根值。
        db_val = 0

        for v in unpacked_data:
            db_val += abs(v)*abs(v)
        # print('sum:{}'.format(db_val))
        db_val = db_val/16
        # 然后开方
        db_val = math.sqrt(db_val)
        # 然后求对数。
        db_val = 20* math.log(db_val/32767,10)
        # 保留一位小数就好了
        db_val = round(db_val, 1)
        # print(unpacked_data)


        if db_val < judgeValue :
            result = '幅值太小({}dB)'.format(db_val)
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
        count = 0
        for i in unpacked_data:
            if abs(i) > Config.LINE_ABS_BASE:
                count = count + 1
        print('超过基准值的点的个数有：{}'.format(count))
        if count > Config.LINE_POINTS:
            result = '降噪不好({},{})，超基准点个数{}'.format(min_val,max_val,count)
            return result
        return '正常，超基准点个数{}'.format(count)

if __name__ == '__main__':
    j = AudioJudge()
    j.judgeSine('input.wav')
