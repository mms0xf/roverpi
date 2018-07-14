class Thlottle:
    # has level
    # level -10 ~ 10
    # return rate -1.0 ~ 1.0

    def __init__(self):
        self.__level  = 0

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        if (self.IsLimit (value)):
            return
        self.__level = value
    
    @property
    def rate(self):
        return float(self.level / 10.0);

    def Reset(self):
            self.level = 0

    def IsLimit( self, amount ):
        if (amount > 10):
            return True
        if (amount < -10):
            return True
        return False

    def StepUp(self):
            self.level+=1

    def StepDown(self):
            self.level-=1


