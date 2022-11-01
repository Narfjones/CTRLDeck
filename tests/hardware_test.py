import unittest
import inc.serialValuetoVolume as run_test

class TestHardware(unittest.TestCase):
    def test_hardware(self):
        """

        Tests that the hardware is present and Serial data is readable
        
        """
        run_test.connectSerial()
        self.assertIsInstance(run_test.chosenPort, int)
        self.assertIsInstance(run_test.numSliders, int)


if __name__ == '__main__':
    unittest.main()