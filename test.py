#!/usr/bin/python

#from tank.gpio_setting import GPIOSetting
#from tank.connected_pin import ConnectedPin
#from tank.wheel import Wheel
from tank.tank_driver import TankDriver
import i2c.grove_i2c_mini_motor_driver as driver

import time
import curses

import asyncio
import math

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



        driver.initialize()

        def on_accel(left_rate, right_rate):

            is_fore_left = (left_rate > 0)
            is_fore_right = (right_rate > 0)
            
            driver.run(1, math.fabs(left_rate), is_fore_left)
            driver.run(2, math.fabs(right_rate), is_fore_right)
            
            KeyControl.screen.clear()
            KeyControl.screen.addstr(10,0,str(left_rate) + ':'+ str(right_rate))
            
        def on_brake():
            driver.stop()
            KeyControl.screen.clear()
            KeyControl.screen.addstr(10,0,'braked')
        
        KeyDrive.tank = TankDriver( on_accel, on_brake )

    @staticmethod
    def _Routine():
        char = KeyControl.screen.getkey()
        if char == ord('q'):
            isQuit = True
            return isQuit
        
    @staticmethod
    def Routine():
        #KeyControl.screen.clear()
        left_fault = driver.get_status(1)
        right_fault = driver.get_status(2)
        KeyControl.screen.addstr(15,0,'left_status  : ' + str(left_fault))
        KeyControl.screen.addstr(16,0,'right_status : ' + str(right_fault))
        
        char = KeyControl.screen.getch()
        if char == ord('q'):
            isQuit = True
            return isQuit

        elif char == curses.KEY_LEFT:
            KeyDrive.tank.TurnLeft()
        elif char == curses.KEY_RIGHT:
            KeyDrive.tank.TurnRight()
        elif char == curses.KEY_UP:
            KeyDrive.tank.Fore()
        elif char == curses.KEY_DOWN:
            KeyDrive.tank.Back()
        elif char == ord(' '):  # space key
            KeyDrive.tank.Brake()

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
        KeyDrive.tank.Brake()



async def sender_routine():
    
    try:
        KeyDrive.Initialize()


        while True:

            
            isQuit = KeyDrive.Routine()
            if isQuit:
                break
            await asyncio.sleep(0.01)
    finally:
        KeyDrive.Finalize()

async def receiver_routine():
    pass
    '''
    while True:
        KeyControl.screen.clear()
        KeyControl.screen.addstr(11,0,'test')
        await asyncio.sleep(0.01)
    '''


async def main_routine():
    #raise ValueError("error!")
    task = asyncio.create_task(sender_routine())
    await task


if __name__ == "__main__":

    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(hello_world())

    # は非同期プログラムのメインのエントリーポイントとして使われるべきで、理想的には 1 回だけ呼び出されるべきです。
    asyncio.run(main_routine())


