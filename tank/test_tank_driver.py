import unittest


from Wheel import Wheel
from ConnectedPin import ConnectedPin
from TankDriver import TankDriver

#need property test !!

class TestTankDriver( unittest.TestCase ):
    def setUp(self):

        pin1 = ConnectedPin( DummyPwm() )
        pin2 = ConnectedPin( DummyPwm() )
        pin3 = ConnectedPin( DummyPwm() )
        pin4 = ConnectedPin( DummyPwm() )
        
        self.left = Wheel( pin1, pin2 )
        self.right = Wheel( pin3, pin4 )
        self.tank = TankDriver( self.left, self.right )

#    def tearDown(self):

    def test_init(self):
        self.assertEqual( False, self.tank.isFore )
        self.assertEqual( False, self.tank.isBack )
        self.assertEqual( False, self.tank.isLeft )
        self.assertEqual( False, self.tank.isRight )
        self.assertEqual( 0, self.tank.throttleAverage )
        self.assertEqual( 0, self.left.duty )
        self.assertEqual( 0, self.right.duty )

    def test_Fore(self):
        self.tank.Fore()
        self.assertEqual( True, self.tank.isFore )
        self.assertEqual( False, self.tank.isBack )
        self.assertEqual( False, self.tank.isLeft )
        self.assertEqual( False, self.tank.isRight )
        self.assertEqual( 1, self.tank.throttleAverage )
        self.assertEqual( 0.1, self.left.duty )
        self.assertEqual( 0.1, self.right.duty )

    def test_Back(self):
        self.tank.Back()
        self.assertEqual( False, self.tank.isFore )
        self.assertEqual( True, self.tank.isBack )
        self.assertEqual( False, self.tank.isLeft )
        self.assertEqual( False, self.tank.isRight )
        self.assertEqual( -1, self.tank.throttleAverage )
        self.assertEqual( -0.1, self.left.duty )
        self.assertEqual( -0.1, self.right.duty )

    def test_TurnLeft(self):
        self.tank.TurnLeft()
        self.assertEqual( False, self.tank.isFore )
        self.assertEqual( False, self.tank.isBack )
        self.assertEqual( True, self.tank.isLeft )
        self.assertEqual( False, self.tank.isRight )
        self.assertEqual( 0.0, self.tank.throttleAverage )
        self.assertEqual( -0.1, self.left.duty )
        self.assertEqual( 0.1, self.right.duty )

    def test_TurnRight(self):
        self.tank.TurnRight()
        self.assertEqual( False, self.tank.isFore )
        self.assertEqual( False, self.tank.isBack )
        self.assertEqual( False, self.tank.isLeft )
        self.assertEqual( True, self.tank.isRight )
        self.assertEqual( 0.0, self.tank.throttleAverage )
        self.assertEqual( 0.1, self.left.duty )
        self.assertEqual( -0.1, self.right.duty )
        
if __name__ == "__main__":
    unittest.main()
#    throttle = TankDriver.Throttle()
#    print throttle.level

            


