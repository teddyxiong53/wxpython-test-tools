#coding: utf-8

from __future__ import print_function
from easyhid import Enumeration

MOUSE=1
SPEAKER=2
DEVICE_TYPE=MOUSE

if DEVICE_TYPE == MOUSE:
    VENDOR_ID  = 0x093a
    PRODUCT_ID  = 0x2510
elif DEVICE_TYPE == SPEAKER:
    VENDOR_ID  = 0xe5b8
    PRODUCT_ID  = 0x0812

class HidWrapper:
    def leftMic(self):
        pass
    def rightMic(self):
        pass
    def RefMic(self):
        pass
    def AecMic(self):
        pass


if __name__ == '__main__':
    en = Enumeration()
    devices = en.find(vid=VENDOR_ID, pid=PRODUCT_ID)

    dev = devices[0]
    print(dev.description())

    dev.open()

    write_data=[0xa0,0x0a]
    len = dev.send_feature_report(write_data)
    # len = dev.write(write_data)
    print("write len:", len)
    read_data=[]

    # read_data = dev.get_feature_report(2)
    # print("read data:", read_data)

    dev.close()
