#import Throttle
from . import Throttle

class TankDriver:
    # DualWheelPwmDriver dualWheel
    # Throttle leftThrottle
    # Throttle rightThrottle

    @property
    def powerText(self):
        return "{0}:{1}".format( self.leftThrottle.level, self.rightThrottle.level)
        
    @property
    def isFore(self):
        return (self.leftThrottle.level + self.rightThrottle.level) > 0

    @property
    def isBack(self):
        return (self.leftThrottle.level + self.rightThrottle.level) < 0


    @property
    def isLeft(self):
        return (self.leftThrottle.level < self.rightThrottle.level);

    @property
    def isRight(self):
        return (self.leftThrottle.level > self.rightThrottle.level)
    
    @property
    def throttleAverage(self):
        # need kiriage
        return int((self.leftThrottle.level + self.rightThrottle.level) / 2.0)


    def __init__( self, leftWheel, rightWheel ):
        self.leftWheel = leftWheel
        self.rightWheel = rightWheel
        self.leftThrottle = Throttle()
        self.rightThrottle = Throttle()


    def Brake(self):
        self.leftThrottle.Reset ()
        self.rightThrottle.Reset ()
        self.leftWheel.Free()
        self.rightWheel.Free()

    def Fore(self):
        if (self.isBack) :
            self.Brake ()
            return
    
        self.leftThrottle.StepUp ()
        self.rightThrottle.StepUp ()
        self.leftWheel.Accel(self.leftThrottle.rate)
        self.rightWheel.Accel(self.rightThrottle.rate)

    def Back(self):
        if (self.isFore) :
            self.Brake ()
            return

        self.leftThrottle.StepDown ()
        self.rightThrottle.StepDown ()

        self.leftWheel.Accel(self.leftThrottle.rate)
        self.rightWheel.Accel(self.rightThrottle.rate)

    def TurnLeft(self):
        if (self.isRight) :
            self.leftThrottle.level = self.throttleAverage
            self.rightThrottle.level = self.throttleAverage
        else :
            self.leftThrottle.StepDown ();
            self.rightThrottle.StepUp ();

        self.leftWheel.Accel(self.leftThrottle.rate)
        self.rightWheel.Accel(self.rightThrottle.rate)

    def TurnRight(self):
        if (self.isLeft):
            self.leftThrottle.level = self.throttleAverage
            self.rightThrottle.level = self.throttleAverage
        else :
            self.leftThrottle.StepUp ()
            self.rightThrottle.StepDown ()

        self.leftWheel.Accel(self.leftThrottle.rate)
        self.rightWheel.Accel(self.rightThrottle.rate)

    def __Log(self):
        left = self.leftThrottle.level
        right = self.rightThrottle.level

        print ("{0} / {1}", left.ToString (), right.ToString ());


