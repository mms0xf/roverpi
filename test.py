#!/usr/bin/python

#from tank.gpio_setting import GPIOSetting
#from tank.connected_pin import ConnectedPin
#from tank.wheel import Wheel
from tank.tank_driver import TankDriver

import time
import curses

import asyncio


class KeyControl:

    @staticmethod
    def Initialize():
        KeyControl.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        KeyControl.screen.nodelay(True)    ##
        KeyControl.screen.keypad(True)

    @staticmethod
    def Finalize():
        curses.nocbreak()
        KeyControl.screen.keypad(0)
        curses.echo()
        curses.endwin()


class KeyDrive:
    @staticmethod
    def Initialize():
        KeyControl.Initialize()

        #GPIOSetting.Initialize()
        #setting = GPIOSetting.setting

        #leftPhasePin = ConnectedPin(setting.leftPhase)
        #leftEnablePin = ConnectedPin(setting.leftEnable)
        #rightPhasePin = ConnectedPin(setting.rightPhase)
        #rightEnablePin = ConnectedPin(setting.rightEnable)

        #left = Wheel( leftPhasePin, leftEnablePin )
        #right = Wheel( rightPhasePin, rightEnablePin )
        #KeyDrive.tank = TankDriver( left, right )

        import i2c.grove_i2c_mini_motor_driver as driver

        driver.initialize()

        def on_accel(left_rate, right_rate):
            print("test")


            is_fore_left = (left_rate > 0)
            is_fore_right = (right_rate > 0)
            
            driver.run(1,left_rate,is_fore_left)
            driver.run(2,right_rate,is_fore_right)
            
            
        def on_brake():
            #left.Free()
            #right.Free()
            driver.stop()
        
        KeyDrive.tank = TankDriver( on_accel, on_brake )

    @staticmethod
    def _Routine():
        char = KeyControl.screen.getkey()
        if char == ord('q'):
            isQuit = True
            return isQuit
        
    @staticmethod
    def Routine():
        char = KeyControl.screen.getch()
        if char == ord('q'):
            isQuit = True
            return isQuit

        elif char == curses.KEY_LEFT:
            KeyControl.screen.clear()
            KeyDrive.tank.TurnLeft()
            KeyControl.screen.addstr(10,0,'left : '+ KeyDrive.tank.powerText)
        elif char == curses.KEY_RIGHT:
            KeyControl.screen.clear()
            KeyDrive.tank.TurnRight()
            KeyControl.screen.addstr(10,0,'right : '+ KeyDrive.tank.powerText)
        elif char == curses.KEY_UP:
            KeyControl.screen.clear()
            KeyDrive.tank.Fore()
            KeyControl.screen.addstr(10,0,'up : '+ KeyDrive.tank.powerText)
        elif char == curses.KEY_DOWN:
            KeyControl.screen.clear()
            KeyDrive.tank.Back()
            KeyControl.screen.addstr(10,0,'down : '+ KeyDrive.tank.powerText)
        elif char == ord(' '):  # space key
            KeyControl.screen.clear()
            KeyDrive.tank.Brake()
            KeyControl.screen.addstr(10,0,'stop : '+ KeyDrive.tank.powerText)

        message = '''
==== manual ======
Allow key : Tank will move. fore, back, turn left, turn right.
Space key : emagency brake
'q' key : quit the application
'''
        KeyControl.screen.addstr(0,0,message)
        
    @staticmethod
    def Finalize():
        KeyControl.Finalize()
        #GPIOSetting.Finalize()
        pass
    

async def sender_routine():
    
    try:
        KeyDrive.Initialize()


        while True:
            isQuit = KeyDrive.Routine()
            if isQuit:
                break
            await asyncio.sleep(0.01)
            #print("Hello World!")
    finally:
        KeyDrive.Finalize()

async def receiver_routine():
    pass
    
    #while True:
    #    await asyncio.sleep(0.01)


async def main_routine():
    #raise ValueError("error!")
    task = asyncio.create_task(sender_routine())
    await task


if __name__ == "__main__":

    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(hello_world())
    print("Go!")
    # は非同期プログラムのメインのエントリーポイントとして使われるべきで、理想的には 1 回だけ呼び出されるべきです。
    asyncio.run(main_routine())
    print("Go2")






'''

'''
