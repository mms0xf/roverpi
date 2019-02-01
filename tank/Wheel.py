import math
#from ConnectedPin import *

class Wheel:

#    @property
#    def isAccelerate(self):
#        return ( self.phasePin.Enabled and not self.enablePin.Enabled )

#    @property
#    def isReverseAccelerate( self ):
#        return ( not self.phasePin.Enabled and self.enablePin.Enabled )

    # return -1 ~ 1
    @property
    def duty(self):
        return self.phasePin.duty - self.enablePin.duty

    def __init__( self,  phasePin,  enablePin ):
        self.phasePin = phasePin
        self.enablePin = enablePin

    def Free(self):
        self.phasePin.Stop()
        self.enablePin.Stop()

    # allow -1 ~ 1
    def Accel(self,duty):
        if duty==0:
            self.Free()
        elif duty < 0:
            self.__BackAccel( math.fabs(duty))
        else:
            self.__ForeAccel( math.fabs(duty))

    # allow 0-1
    def __ForeAccel(self,duty):
        self.phasePin.Emit(duty)
        self.enablePin.Stop()

    #allow 0-1
    def __BackAccel(self,duty):
        self.phasePin.Stop()
        self.enablePin.Emit(duty)

#    def Brake(self):
#        self.phasePin.Enabled = True
#        self.enablePin.Enabled = True





