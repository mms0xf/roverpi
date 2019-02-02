import unittest
from tank.wheel import Wheel
from tank.connected_pin import ConnectedPin
from tank.connected_pin import DummyPwm

#need property test !!

class TestWheelDriver( unittest.TestCase ):
    def setUp(self):
        self.phasePin = ConnectedPin(DummyPwm())
        self.enablePin = ConnectedPin(DummyPwm())
        
        self.wheel = Wheel( self.phasePin, self.enablePin )

#    def tearDown(self):
#        print 'tearDown'

    def test_init(self):
        self.assertEqual( 0, self.phasePin.duty )
        self.assertEqual( 0, self.enablePin.duty )

    def test_Accel(self):
        self.wheel.Accel(2)
        self.assertEqual( 1, self.phasePin.duty )
        self.assertEqual( 0, self.enablePin.duty )
        
        self.wheel.Accel(-2)
        self.assertEqual( 0, self.phasePin.duty )
        self.assertEqual( 1, self.enablePin.duty )

        self.wheel.Accel(0)
        self.assertEqual( 0, self.phasePin.duty )
        self.assertEqual( 0, self.enablePin.duty )

        self.wheel.Accel(0.001)
        self.assertEqual( 0.001, self.phasePin.duty )
        self.assertEqual( 0, self.enablePin.duty )

        self.wheel.Accel(-0.001)
        self.assertEqual( 0, self.phasePin.duty )
        self.assertEqual( 0.001, self.enablePin.duty )

        def test_Free(self):
            self.wheel.Accel(0.5)
            self.wheel.Stop(0)
            self.assertEqual( 0, self.phasePin.duty )
            self.assertEqual( 0, self.enablePin.duty )            
            
if __name__ == "__main__":
    unittest.main()


            


