#import Thlottle
from . import Thlottle # TODO : typo

class TankDriver:
    # DualWheelPwmDriver dualWheel
    # Thlottle leftThlottle
    # Thlottle rightThlottle

    @property
    def powerText(self):
        return "{0}:{1}".format( self.leftThlottle.level, self.rightThlottle.level)
        
    @property
    def isFore(self):
        return (self.leftThlottle.level + self.rightThlottle.level) > 0

    @property
    def isBack(self):
        return (self.leftThlottle.level + self.rightThlottle.level) < 0


    @property
    def isLeft(self):
        return (self.leftThlottle.level < self.rightThlottle.level);

    @property
    def isRight(self):
        return (self.leftThlottle.level > self.rightThlottle.level)
    
    @property
    def thlottleAverage(self):
        # need kiriage
        return int((self.leftThlottle.level + self.rightThlottle.level) / 2.0)


    def __init__( self, leftWheel, rightWheel ):
        self.leftWheel = leftWheel
        self.rightWheel = rightWheel
        self.leftThlottle = Thlottle()
        self.rightThlottle = Thlottle()


    def Brake(self):
        self.leftThlottle.Reset ()
        self.rightThlottle.Reset ()
        self.leftWheel.Free()
        self.rightWheel.Free()

    def Fore(self):
        if (self.isBack) :
            self.Brake ()
            return
    
        self.leftThlottle.StepUp ()
        self.rightThlottle.StepUp ()
        self.leftWheel.Accel(self.leftThlottle.rate)
        self.rightWheel.Accel(self.rightThlottle.rate)

    def Back(self):
        if (self.isFore) :
            self.Brake ()
            return

        self.leftThlottle.StepDown ()
        self.rightThlottle.StepDown ()

        self.leftWheel.Accel(self.leftThlottle.rate)
        self.rightWheel.Accel(self.rightThlottle.rate)

    def TurnLeft(self):
        if (self.isRight) :
            self.leftThlottle.level = self.thlottleAverage
            self.rightThlottle.level = self.thlottleAverage
        else :
            self.leftThlottle.StepDown ();
            self.rightThlottle.StepUp ();

        self.leftWheel.Accel(self.leftThlottle.rate)
        self.rightWheel.Accel(self.rightThlottle.rate)

    def TurnRight(self):
        if (self.isLeft):
            self.leftThlottle.level = self.thlottleAverage
            self.rightThlottle.level = self.thlottleAverage
        else :
            self.leftThlottle.StepUp ()
            self.rightThlottle.StepDown ()

        self.leftWheel.Accel(self.leftThlottle.rate)
        self.rightWheel.Accel(self.rightThlottle.rate)

    def __Log(self):
        left = self.leftThlottle.level
        right = self.rightThlottle.level

        print ("{0} / {1}", left.ToString (), right.ToString ());


