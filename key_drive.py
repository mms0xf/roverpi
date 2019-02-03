#!/usr/bin/python

from tank.gpio_setting import GPIOSetting
from tank.connected_pin import ConnectedPin
from tank.wheel import Wheel
from tank.tank_driver import TankDriver

import time
import curses


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

        GPIOSetting.Initialize()
        setting = GPIOSetting.setting

        leftPhasePin = ConnectedPin(setting.leftPhase)
        leftEnablePin = ConnectedPin(setting.leftEnable)
        rightPhasePin = ConnectedPin(setting.rightPhase)
        rightEnablePin = ConnectedPin(setting.rightEnable)

        left = Wheel( leftPhasePin, leftEnablePin )
        right = Wheel( rightPhasePin, rightEnablePin )
        KeyDrive.tank = TankDriver( left, right )

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
            KeyControl.screen.addstr(10,0,'left : ' + KeyDrive.tank.powerText)
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
        GPIOSetting.Finalize()
    
    
if __name__ == "__main__":    

    try:
        KeyDrive.Initialize()


        
        while True:
            isQuit = KeyDrive.Routine()
            if isQuit:
                break
            time.sleep(0.01)
            
    finally:
        KeyDrive.Finalize()
    
