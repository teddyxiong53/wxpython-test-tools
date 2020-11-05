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
        # 现在都放到这里来做。打开、写入、关闭。
        # 不要一次打开，多次写入。这样在有设备拔插的时候，健壮性很差。
        try:
            en = Enumeration()
            devices = en.find(vid=VENDOR_ID, pid=PRODUCT_ID)
            dev = devices[0]
            dev.open()
            write_data=bytearray(60)
            write_data[0] = value
            len = dev.send_feature_report(write_data,report_id=0x24)
            # len = dev.write(write_data)
            print("write len:", len)
            time.sleep(0.05)
            dev.close()
        except:
            print("写入HID数据失败")
            raise

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
        pass




if __name__ == '__main__':
    pass
