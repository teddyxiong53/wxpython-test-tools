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





testResult = ''



PASS_STR = '正常'



# 创建mainWin类并传入wx_windows.MainFrame
class mainWin(wx_windows.MainFrame):
    testLeftOk = False
    testRightOk = False
    testRefOk = False
    testAecOk = False


    audioJudge = AudioJudge()
    def initAudioWrapper(self):
        try:
            self.audioWrapper = AudioWrapper()
            self.audioWrapper.open()
        except:
            error("打开usb声卡失败")
            self.m_statusBar1.SetStatusText("打开usb声卡失败")

    def initHidWrapper(self):
        self.soundCardOk = False
        self.hidWrapper = HidWrapper()
        if not self.hidWrapper.open():
            self.m_statusBar1.SetStatusText("打开usb声卡失败，请先用usb把音箱连接到电脑")
        else:
            self.soundCardOk = True
            self.m_statusBar1.SetStatusText("")

    def initSystem(self):
        self.initAudioWrapper()
        self.initHidWrapper()
        # self.hidWrapper.startMonitorUsb()

    def testAll(self):
        self.testLeftMic()
        self.testRightMic()
        self.testRef()
        self.testAec()
        if self.testLeftOk and self.testRightOk and self.testRefOk and self.testAecOk:
            self.m_bpButtonResult.SetBitmap(wx.Bitmap('./ok.bmp'))
        else:
            self.m_bpButtonResult.SetBitmap(wx.Bitmap('./fail.bmp'))

    '''
    测试左边mic
    1、先发送hid命令，切换到左mic录音。
    2、用audio自播自录。
    3、分析得到的文件。判断是否合法。
    '''
    def testLeftMic(self):
        # 先清空
        global testLeftOk, testResult
        try:
            self.hidWrapper.leftMic()
        except:
            pass
        self.audioWrapper.setInputFile(INPUT_FILE)
        self.audioWrapper.genOutput(LEFT_FILE)
        self.audioWrapper.waitForFinish()
        result = self.audioJudge.judgeSine(LEFT_FILE)
        if result == PASS_STR:
            testLeftOk = True
        else:
            testLeftOk = False
        testResult = result
        self.m_staticTextLeft.SetLabel(testResult)
        wx.Yield()
    def testRightMic(self):
        global testResult, testRightOk

        self.hidWrapper.rightMic()
        self.audioWrapper.setInputFile(INPUT_FILE)
        self.audioWrapper.genOutput(RIGHT_FILE)
        self.audioWrapper.waitForFinish()
        result = self.audioJudge.judgeSine(RIGHT_FILE)
        if result == PASS_STR:
            testRightOk = True
        else:
            testRightOk = False
        testResult = result

        self.m_staticTextRight.SetLabel(testResult)
        wx.Yield()


    def testRef(self):
        global testResult, testRefOk

        self.hidWrapper.RefMic()
        self.audioWrapper.setInputFile(INPUT_FILE)
        self.audioWrapper.genOutput(REF_FILE)
        self.audioWrapper.waitForFinish()
        result = self.audioJudge.judgeSine(REF_FILE)
        if result == PASS_STR:
            testRefOk = True
        else:
            testRefOk = False
        testResult = result
        self.m_staticTextRef.SetLabel(testResult)
        wx.Yield()
    def testAec(self):
        global testResult, testAecOk
        self.hidWrapper.AecMic()
        self.audioWrapper.setInputFile(MUSIC_FILE)
        self.audioWrapper.genOutput(AEC_FILE)
        self.audioWrapper.waitForFinish()
        result = self.audioJudge.judgeLine(AEC_FILE)
        if result == PASS_STR:
            testAecOk = True
        testResult = result
        self.m_staticTextAec.SetLabel(testResult)
        wx.Yield()
    def OnButtonTestAll(self, event):
        debug('test all')
        self.testAll()


    def OnButtonLeftMic(self, event):
        debug('test left mic')
        self.testLeftMic()



    def OnButtonRightMic(self, event):
        debug('test right mic')
        self.testRightMic()

    def OnButtonRef(self, event):
        debug('test ref ')
        self.testRef()


    def OnButtonAec(self, event):
        debug('test aec')
        self.testAec()



    def OnClose(self, event):
        debug('关闭软件')
        self.audioWrapper.close()
        wx.Exit()

    def OnMenuExit(self, event):
        self.OnClose(event)

    def OnMenuAbout(self, event):
        dialogAbout = wx_windows.DialogAbout(self)
        dialogAbout.m_staticText1.SetLabel(SOFTWARE_NAME+SOFTWARE_VERSION+'\n'+SOFTWARE_AUTHOR)
        dialogAbout.ShowModal()



def initLog():
    logging.basicConfig(filename='test-tools.log', level=logging.DEBUG, format=LOG_FORMAT)



def initAudioJudge():
    pass

def initDir():
    # 如果没有audio_output目录。创建
    if not os.path.exists(AUDIO_OUTPUT_DIR):
        os.mkdir(AUDIO_OUTPUT_DIR)

if __name__ == '__main__':
    initConfig()
    initLog()
    initDir()

    info('打开软件')
    # 下面是使用wxPython的固定用法
    # 这个是把输出重定向到文件里。
    # app = wx.App(redirect=True, filename="output.log")
    app = wx.App()
    main_win = mainWin(None)
    main_win.SetTitle(SOFTWARE_NAME + SOFTWARE_VERSION)
    main_win.Show()
    main_win.initSystem()
    app.MainLoop()
