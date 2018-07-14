import RPi.GPIO

class ConnectedPin:

    def __init__(self, pwm):
        self.pwm = pwm
        self.duty = 0.0

    @property
    def isEmitting(self):
        return self.duty != 0.0

    @property
    def duty(self):
        return self.duty

    def Emit(self, rate):

        if rate < 0:
            rate = 0
        if rate > 1:
            rate = 1
        
        self.duty = rate
        self.pwm.ChangeDutyCycle(rate * 100)

    def Stop(self):
        self.Emit( 0.0 )
        
class DummyPwm:
    def ChangeDutyCycle(self,rate) : 
        self.rate = rate        
