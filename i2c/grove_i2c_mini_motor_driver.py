# https://qiita.com/coppercele/items/15d4290146cb936e90ed
# https://www.denshi.club/pc/python/iotpythonstep1xx.html




import smbus
import time
i2c = smbus.SMBus(1)  #1 : bus number

 
#define FAULT 0x01 //レジスタのサブドレス

#DEFAULT ADDR1:0xCA(W) 0xCB(R)
#DEFAULT ADDR2:0xC0(W) 0xC1(R)

#CA 11001010
#C0 11000000

#111111 01

'''
000110
3F
0011 1111

000000 00 ←停止

min - max
000110<->111111
111111 01 ←正転5V
100101 10 ←逆転3V
000000 11 ←ブレーキ
'''

'''
0x60
0x65
RaspberryPiでもシフト必要
by i2sdetect-y 1の結果より
'''

rightWrite= 0x65 # 0xca
rightRead= 0x66 # 0xcb

leftWrite = 0x60 # 0xC0
leftRead = 0x61 # 0xC1

_command=0x00


_accel = 0b11111101 # 5v

i2c.write_byte_data(leftWrite, _command, _accel)
i2c.write_byte_data(rightWrite, _command, _accel)
time.sleep(10)
i2c.write_byte_data(leftWrite, _command, 0)
i2c.write_byte_data(rightWrite, _command, 0)


#define FAULT 0x01  // 00000001
#define CLEAR 0x80  // 10000000
#define ILIMIT 0x10 // 00010000 電流制限
#define OTS 0x08    // 00001000 過熱
#define UVLO 0x04   // 00000100 低電圧誤動作防止
#define OCP 0x02    // 00000010　過電流

_clear = 0b10000000
fallt_mask = 0b00000001
limit_mask = 0b00010000
ots_mask = 0b00001000
uvlo_mask = 0b00000100
ocp_mask = 0b00000010
'''
while 1:
    res = read_byte_data(rightRead, _command)
    if (res&fault_mask):
        if (res&limit_mask):
            print('current limitation')
        if (res&ots_mask):
            print('over tempture state')
        if (res&ots_mask):
            print('over tempture state')
        if (res&uvlo_mask):
            print('over tempture state')
        if (res&ocp_mask):
            print('over current')
        # clear error status
        i2c.write_byte_data(rightWrite, _command, _clear)
    
    
    
    time.sleep(1)
'''
