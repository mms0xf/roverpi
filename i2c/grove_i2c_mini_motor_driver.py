# https://qiita.com/coppercele/items/15d4290146cb936e90ed
# https://www.denshi.club/pc/python/iotpythonstep1xx.html




import smbus
import time
import enum

 
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

000110(06) minSpeed
111111(3F) maxSpeed
'''

'''
0x60
0x65
RaspberryPiでもシフト必要
by i2sdetect-y 1の結果より
'''

#ch1
channel1_write= 0x65 # 0xca
channel1_read= 0x66 # 0xcb

#ch2
channel2_write = 0x60 # 0xC0
leftRead = 0x61 # 0xC1

_command=0x00


_accel = 0b11111101 # 5v

_minSpeed = 0b000110 #(06)
_maxSpeed = 0b111111 #(3F)

_fore = 0b01
_back = 0b10

# get direction bit (fore/back)
def _direction_bit(is_fore):
    # fore : 01
    # back : 10
    if is_fore is True:
        return _fore
    else:
        return _back

# get speed bit for vset from 0.0-1.0 range
def _speed_bit(speed_rate):# 0-1
    if speed_rate < 0:
        speed_rate = 0
        
    if speed_rate > 1:
        speed_rate = 1

    length = _maxSpeed - _minSpeed
    
    speed_bit = int(length * speed_rate) + _minSpeed

    
    return speed_bit

def _merge_speed_and_direction(speed_bit, dir_bit):
    return (speed_bit << 2) + dir_bit

# get writing channel address from 1 or 2
def _writing_channel_bit(channel_no):
    if channel_no == 1:
        return channel1_write
    elif channel_no == 2:
        return channel2_write
    else:
        raise ValueError("unsupperted channel no")
        
def run(channel_no, speed_rate, is_fore):

    speed = _speed_bit(speed_rate)
    dir = _direction_bit(is_fore)

    accel_bit = _merge_speed_and_direction(speed, dir)

    channel_bit = _writing_channel_bit(channel_no)
    i2c.write_byte_data(channel_bit, _command, accel_bit)




def stop():
    i2c.write_byte_data(channel2_write, _command, 0)
    i2c.write_byte_data(channel1_write, _command, 0)



_clear = 0b10000000
fallt_mask = 0b00000001
limit_mask = 0b00010000 # 電流制限
ots_mask = 0b00001000 # 過熱
uvlo_mask = 0b00000100 # 低電圧誤動作防止
ocp_mask = 0b00000010 # 過電流


# reset
def reset_error(channel_no):
    channel_address = _writing_channel_bit(channel_no)
    i2c.write_byte_data(channel_address, _command, _clear)

# enum
class Fault(enum.Enum):
    CURRENT_LIMITATION=enum.auto()
    OVER_TEMPTURE=enum.auto()
    PREVENT_LOW_VOLTAGE_OPERATION=enum.auto()
    OVER_CURRENT=enum.auto()


# get status. use on the endless loop.
def get_status(channel_no):
    channel_address = _writing_channel_bit(channel_no)
    res = read_byte_data(channel_address, _command)
    if (res&fault_mask):
        if (res&limit_mask):
            return Fault.CURRENT_LIMITATION
        if (res&ots_mask):
            return Fault.OVER_TEMPTURE
        if (res&uvlo_mask):
            return Fault.PREVENT_LOW_VOLTAGE_OPERATION
        if (res&ocp_mask):
            return Fault.OVER_CURRENT
def initialize(): 
    pass


i2c = smbus.SMBus(1)  #1 : bus number, fixed on raspberry pi

if __name__ == "__main__":

    initialize()

    # left
    run(channel_no=1, speed_rate=0.2, is_fore=True)
    
    # right
    run(channel_no=2, speed_rate=0.2, is_fore=True)
    
    time.sleep(10)
    stop()
