from unittest import TestCase

import main


class MainTests(TestCase):
    def test_result(self):
        self.assertEqual(main.isSpam("https://goo.gl/nVLutc", ["www.filekok.com"], 1), False)
        self.assertEqual(main.isSpam("https://goo.gl/nVLutc", ["bit.ly"], 1), True)
        self.assertEqual(main.isSpam("https://goo.gl/nVLutc", ["tvtv24.com"], 2), True)
        self.assertEqual(main.isSpam("https://goo.gl/nVLutc", ["www.filekok.com"], 2), False)
        self.assertEqual(main.isSpam("https://goo.gl/nVLutc", ["www.filekok.com"], 3), True)
