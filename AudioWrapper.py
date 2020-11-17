#coding: utf-8

from __future__ import print_function
import pyaudio
import wave
import threading

from logging import debug, error, info

from Config import *

import wx

print = debug

class AudioWrapper():
    def __init__(self):
        pass


    def record(self):
        self.recordThread = threading.Thread(target=self.recordThreadProc)
        self.recordThread.start()
        print("begin record")
        
    def recordThreadProc(self):
        # 先清空，这个是为了保证反复录音的时候，数据正常。
        self.readFrames = []
        self.readStream.start_stream()
        data = self.readStream.read(CHUNK)
        # 录音不出问题，是一直可以录下去的。
        # 所以需要通过播放是否完成来控制是否继续录音。
        while data and self.isPlaying and  self.testingFlag:
            # print("len:", len(data))
            self.readFrames.append(data)
            data = self.readStream.read(CHUNK)
        self.readStream.stop_stream()

        print("end of record")
        # 接下来，把录音数据写成wav文件。
        # 这样就可以把步骤分得比较清晰，而且wav文件也可以用其他软件打开来分析。
        print('begin to write data to outfile')
        self.outputWaveFile = wave.open(self.outputFile, 'wb')
        if not self.outputWaveFile:
            print("open output file" + self.outputFile + " fail")
            return
        self.outputWaveFile.setnchannels(CHANNELS)
        self.outputWaveFile.setsampwidth(self.pa.get_sample_size(FORMAT))
        self.outputWaveFile.setframerate(RATE)
        self.outputWaveFile.writeframes(b''.join(self.readFrames))
        self.outputWaveFile.close()
        print('end of write output wav file')


    def play(self):
        self.isPlaying = True
        self.playThread = threading.Thread(target=self.playThreadProc)
        self.playThread.start()
        print("begin play")

    def playThreadProc(self):
        self.inputWaveFile = wave.open(self.inputFile)
        if not self.inputWaveFile:
            error("open wav file fail")
            return False

        self.writeStream.start_stream()
        data = self.inputWaveFile.readframes(CHUNK)

        while data and  self.testingFlag:
            self.writeStream.write(data)
            data = self.inputWaveFile.readframes(CHUNK)

        self.writeStream.stop_stream()

        self.isPlaying = False
        self.inputWaveFile.close()
    # 用这个做对外接口。
    def genOutput(self, outfile, testingFlag):
        self.pa = pyaudio.PyAudio()
        self.writeStream = None
        self.readFrames = []
        # self.inputFile = INPUT_FILE
        self.isPlaying = False

        self.outputFile = outfile
        self.open()
        self.testingFlag = testingFlag
        self.play()
        self.record()

    def waitForFinish(self):
        self.playThread.join()
        self.recordThread.join()
        self.close()

    def close(self):
        try:
            if self.writeStream:
                self.writeStream.close()
            if self.readStream:
                self.readStream.close()
            if self.pa:
                self.pa.terminate()
        except:
            print("关闭出错了")

    def setInputFile(self, filename):
        self.inputFile = filename

    def open(self):
        self.writeStream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            # input=True,
            output=True,
            frames_per_buffer=CHUNK
        )
        self.readStream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            # output=True,
            frames_per_buffer=CHUNK
        )
if __name__ == '__main__':

    print("end of code")


