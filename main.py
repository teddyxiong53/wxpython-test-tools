# coding: utf-8
from __future__ import print_function
import wx
import wx_windows
import logging
from logging import debug, error, info
from AudioWrapper import AudioWrapper
from HidWrapper import HidWrapper
from AudioJudge import AudioJudge
from Config import *

import sys, os



audioWrapper = AudioWrapper()
hidWrapper = HidWrapper()
audioJudge = AudioJudge()

testResult = ''


def testAll():
    testLeftMic()
    testRightMic()
    testRef()
    testAec()


'''
测试左边mic
1、先发送hid命令，切换到左mic录音。
2、用audio自播自录。
3、分析得到的文件。判断是否合法。
'''
def testLeftMic():
    # 先清空
    global testResult
    testResult = '左MIC：'
    hidWrapper.leftMic()
    audioWrapper.setInputFile(INPUT_FILE)
    audioWrapper.genOutput(LEFT_FILE)
    audioWrapper.waitForFinish()
    result = audioJudge.judgeSine(LEFT_FILE)
    testResult += result
    testResult += ' '

def testRightMic():
    global testResult
    testResult += '右MIC：'
    hidWrapper.rightMic()
    audioWrapper.setInputFile(INPUT_FILE)
    audioWrapper.genOutput(RIGHT_FILE)
    audioWrapper.waitForFinish()
    result = audioJudge.judgeSine(RIGHT_FILE)
    testResult += result
    testResult += ' '


def testRef():
    global testResult
    testResult += 'REF：'
    hidWrapper.RefMic()
    audioWrapper.setInputFile(INPUT_FILE)
    audioWrapper.genOutput(REF_FILE)
    audioWrapper.waitForFinish()
    result = audioJudge.judgeSine(REF_FILE)
    testResult += result
    testResult += ' '

def testAec():
    global testResult
    testResult += 'AEC：'
    hidWrapper.AecMic()
    audioWrapper.setInputFile(MUSIC_FILE)
    audioWrapper.genOutput(AEC_FILE)
    audioWrapper.waitForFinish()
    result = audioJudge.judgeLine(AEC_FILE)
    testResult += result
    testResult += ' '


# 创建mainWin类并传入wx_windows.MainFrame
class mainWin(wx_windows.MainFrame):
    def OnButtonTestAll(self, event):
        debug('test all')
        testAll()
        self.m_textCtrlInfo.SetValue(testResult)

    def OnButtonLeftMic(self, event):
        debug('test left mic')
        testLeftMic()
        self.m_textCtrlInfo.SetValue(testResult)

    def OnButtonRightMic(self, event):
        debug('test right mic')
        testRightMic()
        self.m_textCtrlInfo.SetValue(testResult)
    def OnButtonRef(self, event):
        debug('test ref ')
        testRef()
        self.m_textCtrlInfo.SetValue(testResult)
    def OnButtonAec(self, event):
        debug('test aec')
        testAec()
        self.m_textCtrlInfo.SetValue(testResult)

    def OnClose(self, event):
        debug('关闭软件')
        audioWrapper.close()
        wx.Exit()

    def OnMenuExit(self, event):
        self.OnClose(event)

    def OnMenuAbout(self, event):
        dialogAbout = wx_windows.DialogAbout(self)
        dialogAbout.ShowModal()



def initLog():
    logging.basicConfig(filename='test-tools.log', level=logging.DEBUG, format=LOG_FORMAT)

def initAudioWrapper():
    pass

def initHidWrapper():
    pass

def initAudioJudge():
    pass

def initDir():
    # 如果没有audio_output目录。创建
    if not os.path.exists(AUDIO_OUTPUT_DIR):
        os.mkdir(AUDIO_OUTPUT_DIR)

if __name__ == '__main__':
    initLog()
    initDir()
    initAudioWrapper()
    initHidWrapper()
    info('打开软件')
    # 下面是使用wxPython的固定用法
    app = wx.App()

    main_win = mainWin(None)

    main_win.Show()

    app.MainLoop()
