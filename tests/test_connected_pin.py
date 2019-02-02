import unittest
from tank.connected_pin import ConnectedPin
from tank.connected_pin import DummyPwm

class TestConnectedPin( unittest.TestCase ):
    def setUp(self):
        self.pin = ConnectedPin( DummyPwm() )

#    def tearDown(self):

    def test_init(self):   
        self.assertEqual( False, self.pin.isEmitting )
        self.assertEqual( 0.0, self.pin.duty )

    def test_Emit(self):
        self.pin.Emit( 0.6 )
        self.assertEqual( True, self.pin.isEmitting )
        self.assertEqual( 0.6, self.pin.duty )

        self.pin.Emit( 0.0 )
        self.assertEqual( False, self.pin.isEmitting )
        self.assertEqual( 0.0, self.pin.duty )

        self.pin.Emit( -3.0 )
        self.assertEqual( False, self.pin.isEmitting )
        self.assertEqual( 0.0, self.pin.duty )

        self.pin.Emit( 1.1 )
        self.assertEqual( True, self.pin.isEmitting )
        self.assertEqual( 1.0, self.pin.duty )


    def test_Stop(self):
        self.pin.Emit( 0.6 )
        self.pin.Stop(  )
        self.assertEqual( False, self.pin.isEmitting )
        self.assertEqual( 0.0, self.pin.duty )


if __name__ == "__main__":
    unittest.main()
