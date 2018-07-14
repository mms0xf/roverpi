#!/usr/bin/python

import RPi.GPIO as GPIO
import time

class GPIOSetting:

    def __init__(self, leftPhase,leftEnable, rightPhase, rightEnable):
        self.leftPhase=leftPhase
        self.leftEnable=leftEnable
        self.rightPhase=rightPhase
        self.rightEnable=rightEnable
        self.pwms = [leftPhase,leftEnable, rightPhase, rightEnable]

        for pwm in self.pwms:
            pwm.start(0)    # minimum On when low frequency
            print "pwm initialized"
            #pwm.stop()

    @staticmethod        
    def Initialize():
        GPIO.setmode(GPIO.BOARD)

        # 37	out     vcc immediate

        # 35	out	B Enable2
        # 33	out	B Phase1 

        # 31	out	A Enable2
        # 29	out	A Phase1

        vccPin= 37
        leftWheelPins = [33,35]
        rightWheelPins = [29,31]
        GPIO.setup( vccPin, GPIO.OUT )
        GPIO.setup( leftWheelPins, GPIO.OUT )
        GPIO.setup( rightWheelPins, GPIO.OUT )

        GPIO.output( vccPin, True )

        GPIOSetting.setting = GPIOSetting(GPIO.PWM(33,100),GPIO.PWM(35,100),GPIO.PWM(29,100),GPIO.PWM(31,100))

    @staticmethod
    def Finalize():
        GPIO.cleanup()
        print 'GPIO.cleanup()'

    @staticmethod
    def test():
        print 'pwm left'
        time.sleep(1)
        GPIOSetting.setting.leftPhase.ChangeDutyCycle(20)
        time.sleep(1)
        GPIOSetting.setting.leftPhase.ChangeDutyCycle(66)
        time.sleep(1)
        GPIOSetting.setting.leftPhase.ChangeDutyCycle(99)
        

###################################
#if __name__ == "__main__":
#    try:
#        GPIOSetting.Initialize()
#        GPIOSetting.test()


#    finally:
#        GPIOSetting.Finalize()

    
    
