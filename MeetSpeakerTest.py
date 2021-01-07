# coding: utf-8
from __future__ import print_function
import wx
import wx_windows
import logging
from logging import debug, error, info
from AudioWrapper import AudioWrapper
from HidWrapper import HidWrapper
from AudioJudge import AudioJudge
# from Config import *
import Config

import sys, os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



testResult = ''



PASS_STR = '正常'

OPEN_FAIL_STR = '打开USB声卡失败，请确认用USB连接音箱到电脑后再重试'
OPEN_OK_STR = '打开USB声卡成功'


TEST_ALL_START = '一键测试所有'
TEST_ALL_STOP = '停止'

# 创建mainWin类并传入wx_windows.MainFrame
class mainWin(wx_windows.MainFrame):
    testLeftOk = False
    testRightOk = False
    testRefOk = False
    testAecOk = False

    # 在点击开始测试所有后，可以按键停下来。
    # stopAll = False
    # 是否正在进行测试所有的操作。
    isTestingAll = False

    audioJudge = AudioJudge()
    def initAudioWrapper(self):
        self.audioWrapper = AudioWrapper()



    def initHidWrapper(self):
        self.soundCardOk = False
        self.hidWrapper = HidWrapper()


    def initSystem(self):
        self.initAudioWrapper()
        self.initHidWrapper()


    def testAll(self):
        if self.isTestingAll:
            self.isTestingAll = False
            self.m_buttonTestAll.SetLabelText(TEST_ALL_START)
            # 需要进行停止操作
            wx.Yield()
            return
        self.m_staticTextLeft.SetLabel("")
        self.m_staticTextRight.SetLabel("")
        self.m_staticTextRef.SetLabel("")
        self.m_staticTextAec.SetLabel("")

        self.isTestingAll = True
        self.testLeftMic(True)
        self.testRightMic(True)
        self.testRef(True)
        self.testAec(True)
        # self.testLeftOk = True;self.testRightOk = True; self.testRefOk =True; self.testAecOk = True
        if self.testLeftOk and self.testRightOk and self.testRefOk and self.testAecOk:
            self.m_bpButtonResult.SetBitmap(wx.Bitmap('./ok.bmp'))
        else:
            self.m_bpButtonResult.SetBitmap(wx.Bitmap('./fail.bmp'))
        # 测试所有完成后，把标志设置一下。
        self.isTestingAll = False
        self.m_buttonTestAll.SetLabelText(TEST_ALL_START)
        # 这里必须yield一下，不然测试过了，界面也不会刷新的。
        wx.Yield()
    '''
    测试左边mic
    1、先发送hid命令，切换到左mic录音。
    2、用audio自播自录。
    3、分析得到的文件。判断是否合法。
    '''
    def testLeftMic(self, fromTestAll=False):
        # 先清空
        global testLeftOk, testResult
        try:
            self.hidWrapper.leftMic()
        except:
            # 出错了。然后就设置状态栏，返回
            self.m_statusBar1.SetStatusText(OPEN_FAIL_STR)
            return
        if fromTestAll:
            # 如果是点击测试所有而调用的这个。
            # 那么就把测试所有的按钮，在这里改成停止
            if self.isTestingAll:
                self.m_buttonTestAll.SetLabelText(TEST_ALL_STOP)
        debug('-------------------------测试左MIC')
        self.m_statusBar1.SetStatusText(OPEN_OK_STR)
        self.audioWrapper.setInputFile(Config.INPUT_FILE)
        if fromTestAll:
            self.audioWrapper.genOutput(Config.LEFT_FILE, self.isTestingAll)
        else:
            self.audioWrapper.genOutput(Config.LEFT_FILE, True)

        self.audioWrapper.waitForFinish()
        result = self.audioJudge.judgeSine(Config.LEFT_FILE, Config.SINE_ABS_BASE)
        if result == PASS_STR:
            self.testLeftOk = True
        else:
            self.testLeftOk = False
        testResult = result

        if self.testLeftOk:
            self.m_staticTextLeft.SetBackgroundColour(wx.GREEN)
        else:
            self.m_staticTextLeft.SetBackgroundColour(wx.RED)
        self.m_staticTextLeft.SetLabel(testResult)
        wx.Yield()

    def testRightMic(self, fromTestAll=False):
        global testResult, testRightOk
        try:
            self.hidWrapper.rightMic()
        except:
            # 出错了。然后就设置状态栏，返回
            self.m_statusBar1.SetStatusText(OPEN_FAIL_STR)
            return
        debug('--------------------------测试右MIC')
        self.m_statusBar1.SetStatusText(OPEN_OK_STR)
        self.audioWrapper.setInputFile(Config.INPUT_FILE)
        if fromTestAll:
            self.audioWrapper.genOutput(Config.RIGHT_FILE, self.isTestingAll)
        else:
            self.audioWrapper.genOutput(Config.RIGHT_FILE, True)

        self.audioWrapper.waitForFinish()
        if fromTestAll and not self.isTestingAll:
            wx.Yield()
            return

        result = self.audioJudge.judgeSine(Config.RIGHT_FILE, Config.SINE_ABS_BASE)
        if result == PASS_STR:
            self.testRightOk = True
        else:
            self.testRightOk = False
        testResult = result
        if self.testRightOk:
            self.m_staticTextRight.SetBackgroundColour(wx.GREEN)
        else:
            self.m_staticTextRight.SetBackgroundColour(wx.RED)
        self.m_staticTextRight.SetLabel(testResult)
        wx.Yield()

    def showPic(self):
        # 先杀掉所有的看图进程。
        # 把图片画好。
        # 然后显示其中一张，可以左右来查看。
        # return
        from AudioJudge import left_y_data, right_y_data, ref_y_data, aec_y_data
        #解决中文显示问题
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.title('测试结果音频波形')

        plt.subplot(2,2,1, title='左mic')
        plt.plot(left_y_data)


        plt.subplot(2,2,2, title='右mic')
        plt.plot(right_y_data)


        plt.subplot(2,2,3, title='ref信号')
        plt.plot(ref_y_data)

        plt.subplot(2,2,4, title='AEC')
        plt.plot(aec_y_data)

        plt.savefig('plot.png', dpi=100)
        plt.close()
        os.system("explorer.exe plot.png")

    def testRef(self, fromTestAll=False):
        global testResult, testRefOk
        try:
            self.hidWrapper.RefMic()
        except:
            # 出错了。然后就设置状态栏，返回
            self.m_statusBar1.SetStatusText(OPEN_FAIL_STR)
            return
        debug('-------------------------测试REF')
        self.audioWrapper.setInputFile(Config.INPUT_FILE)
        if fromTestAll:
            self.audioWrapper.genOutput(Config.REF_FILE, self.isTestingAll)
        else:
            self.audioWrapper.genOutput(Config.REF_FILE, True)

        self.audioWrapper.waitForFinish()
        if fromTestAll and not self.isTestingAll:
            wx.Yield()
            return
        result = self.audioJudge.judgeSine(Config.REF_FILE, Config.REF_SINE_ABS_BASE)
        if result == PASS_STR:
            self.testRefOk = True
        else:
            self.testRefOk = False
        testResult = result
        if self.testRefOk:
            self.m_staticTextRef.SetBackgroundColour(wx.GREEN)
        else:
            self.m_staticTextRef.SetBackgroundColour(wx.RED)
        self.m_staticTextRef.SetLabel(testResult)
        wx.Yield()

    def testAec(self, fromTestAll=False):
        global testResult, testAecOk
        try:
            self.hidWrapper.AecMic()
        except:
            # 出错了。然后就设置状态栏，返回
            self.m_statusBar1.SetStatusText(OPEN_FAIL_STR)
            return
        self.m_statusBar1.SetStatusText(OPEN_OK_STR)

        debug('----------------------------测试AEC')
        self.audioWrapper.setInputFile(Config.MUSIC_FILE)
        if fromTestAll:
            self.audioWrapper.genOutput(Config.AEC_FILE, self.isTestingAll)
        else:
            self.audioWrapper.genOutput(Config.AEC_FILE, True)

        self.audioWrapper.waitForFinish()

        if fromTestAll and not self.isTestingAll:
            wx.Yield()
            return

        result = self.audioJudge.judgeLine(Config.AEC_FILE)
        print(result)
        if result == PASS_STR:
            self.testAecOk = True
        else:
            self.testAecOk = False
        testResult = result
        if self.testAecOk:
            self.m_staticTextAec.SetBackgroundColour(wx.GREEN)
        else:
            self.m_staticTextAec.SetBackgroundColour(wx.RED)
        self.m_staticTextAec.SetLabel(testResult)
        wx.Yield()
    def OnButtonTestAll(self, event):
        debug('-----------------一键测试所有')
        self.testAll()


    def OnButtonLeftMic(self, event):

        self.testLeftMic()



    def OnButtonRightMic(self, event):

        self.testRightMic()

    def OnButtonRef(self, event):

        self.testRef()

    def OnButtonShowPic( self, event ):
        self.showPic()

    def OnButtonAec(self, event):

        self.testAec()



    def OnClose(self, event):
        debug('关闭软件')
        self.audioWrapper.close()
        wx.Exit()

    def OnMenuExit(self, event):
        self.OnClose(event)

    def OnMenuAbout(self, event):
        dialogAbout = wx_windows.DialogAbout(self)
        dialogAbout.m_staticText1.SetLabel(Config.SOFTWARE_NAME+Config.SOFTWARE_VERSION+'\n'+Config.SOFTWARE_AUTHOR)
        dialogAbout.ShowModal()

    def OnOpenLog( self, event ):
        if os.path.exists('test-tools.log'):
            os.system("notepad.exe test-tools.log")

    def OnOpenParam( self, event ):
        if os.path.exists('param.json'):
            os.system("notepad.exe param.json")
    def OnClearLog( self, event ):
        if os.path.exists('test-tools.log'):
            open("test-tools.log", 'w').close() # 这一行代码就是清空文件

def initLog():
    logging.basicConfig(filename='test-tools.log', level=logging.DEBUG, format=Config.LOG_FORMAT)



def initAudioJudge():
    pass

def initDir():
    # 如果没有audio_output目录。创建
    if not os.path.exists(Config.AUDIO_OUTPUT_DIR):
        os.mkdir(Config.AUDIO_OUTPUT_DIR)

if __name__ == '__main__':
    print("before load json:", Config.SINE_ABS_BASE)
    Config.initConfig()
    print("after load json:", Config.SINE_ABS_BASE)
    initLog()
    initDir()

    info('打开软件')
    # 下面是使用wxPython的固定用法
    # 这个是把输出重定向到文件里。
    # app = wx.App(redirect=True, filename="output.log")
    app = wx.App()
    main_win = mainWin(None)
    main_win.SetTitle(Config.SOFTWARE_NAME + Config.SOFTWARE_VERSION)
    main_win.Show()
    main_win.initSystem()
    app.MainLoop()
