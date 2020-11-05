#coding: utf-8

from __future__ import print_function
from easyhid import Enumeration
import time
import threading

MOUSE=1
SPEAKER=2
DEVICE_TYPE=SPEAKER

if DEVICE_TYPE == MOUSE:
    VENDOR_ID  = 0x093a
    PRODUCT_ID  = 0x2510
elif DEVICE_TYPE == SPEAKER:
    VENDOR_ID  = 0xe5b8
    PRODUCT_ID  = 0x0812


MODE_TEST=0xf1

MODE_TEST_LEFT=0xf2
MODE_TEST_RIGHT=0xf3



MODE_TEST_REF=0xf4
MODE_TEST_AEC=0xf5

class HidWrapper:
    inTestMode = False
    def writeReport(self, value):
        write_data=bytearray(60)
        write_data[0] = value
        len = self.dev.send_feature_report(write_data,report_id=0x24)
        # len = dev.write(write_data)
        print("write len:", len)
        time.sleep(0.05)

    def leftMic(self):
        if not self.inTestMode:
            self.enterTestMode()
        self.writeReport(MODE_TEST_LEFT)

    def rightMic(self):
        if not self.inTestMode:
            self.enterTestMode()
        self.writeReport(MODE_TEST_RIGHT)

    def RefMic(self):
        if not self.inTestMode:
            self.enterTestMode()
        self.writeReport(MODE_TEST_REF)

    def AecMic(self):
        if not self.inTestMode:
            self.enterTestMode()
        self.writeReport(MODE_TEST_AEC)

    def enterTestMode(self):
        self.writeReport(MODE_TEST)
        inTestMode = True

    def open(self):
        self.en = Enumeration()
        self.devices = self.en.find(vid=VENDOR_ID, pid=PRODUCT_ID)
        if self.devices:
            self.dev = self.devices[0]
        else:
            self.dev = None
            print("dev is None")
        # print(dev.description())
        if self.dev:
            self.dev.open()
            return True
        else:
            return False
        # 进入测试模式

    def startMonitorUsb(self):
        self.monitorThread = threading.Thread(target=self.monitorThreadProc)
        self.monitorThread.start()

    def monitorThreadProc(self):
        invalid = False
        while True:
            time.sleep(0.5)
            try:
                if self.dev:
                    # 尝试获取一下信息，如果被拔掉了，那么就会出错。
                    print(self.dev.get_product_string())
                    print("is valid")
                    invalid = False
            except:
                print("设备失效了")
                # 怎样补救？
                invalid = True

            # 尝试关闭再打开
            if invalid:
                self.devices = self.en.find(vid=VENDOR_ID, pid=PRODUCT_ID)
                if self.devices:
                    self.dev = self.devices[0]
                    print("重新打开，再次发现了设备")
                else:
                    self.dev = None
                if self.dev:
                    if self.dev.is_open():
                        self.dev.close()
                    self.dev.open()

if __name__ == '__main__':
    pass
