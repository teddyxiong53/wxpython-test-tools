# 这个是工具，计算以某个只为幅值的正弦波信号的db值。
import math
def calc_db(data):
    db_val = 0

    for v in data:
        db_val += abs(v)*abs(v)
    # print('sum:{}'.format(db_val))
    db_val = db_val/16
    # 然后开方
    db_val = math.sqrt(db_val)
    # 然后求对数。
    db_val = 20* math.log(db_val/32767,10)
    # 保留一位小数就好了
    db_val = round(db_val, 1)
    return db_val

def gen_sine_data(max_val):
    i=0
    list1=[]  #定义一个空list
    while(i<360):
        list1.append(i)  #把数据增加到列表末
        i=i+22.5; #因为我要一个周期里有100个点，所以点间距为3.6度

    #以上生成了100个点的角度数据
    list2=[x*math.pi/180 for x in list1]  #把角度转成弧度

    list3=[max_val*math.sin(x) for x in list2]  #求出正弦值,并放大100倍

    list4=[int(x) for x in list3] #取整

    # print(list4)
    return list4

# d = gen_sine_data(1500)
# db = calc_db(d)
# print(db)
#
# d = gen_sine_data(16384)
# db = calc_db(d)
# print(db)

# 把1000到2000对应的dB值都得出来
for i in range(10):
    val = 1000+i*100
    # print('max val:{}'.format(val))
    d = gen_sine_data(val)
    db= calc_db(d)
    print('{},{}'.format(val,db))
