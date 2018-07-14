import unittest
from Thlottle import *

class TestThlottle( unittest.TestCase ):
    def setUp(self):
        self.throttle = Thlottle()

#    def tearDown(self):


    def test_Limit(self):
        
        self.assertEqual( True, self.throttle.IsLimit( 11) )
        self.assertEqual( False, self.throttle.IsLimit( 10) )
        self.assertEqual( False, self.throttle.IsLimit(-10) )
        self.assertEqual( True, self.throttle.IsLimit( -11) )

    def test_StepUp(self):
        self.throttle.level = 33
        self.throttle.StepUp()
        self.assertEqual( 34, self.throttle.level ) # no
        self.throttle.StepDown()
        self.assertEqual( 33, self.throttle.level ) # no

        self.throttle.Reset()
        self.assertEqual( 0, self.throttle.level )

    def test_rate(self):
        self.throttle.level = 0
        self.assertEqual( 0, self.throttle.rate )
        
        self.throttle.level = 5
        self.assertEqual( 0.5, self.throttle.rate )

        self.throttle.level = 10
        self.assertEqual( 1, self.throttle.rate )

        self.throttle.level = -5
        self.assertEqual( -0.5, self.throttle.rate )

        self.throttle.level = -10
        self.assertEqual( -1, self.throttle.rate )


if __name__ == "__main__":
    unittest.main()
