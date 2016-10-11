import unittest
import slip

class SLIPDecoderTestCase(unittest.TestCase):
    def test_end_marker(self):
        """
        Check that the packets are delimited by the end marker.
        """
        data = bytes((0x42, 0x34, slip.END))
        self.assertEqual(next(slip.decode(data)), bytes((0x42, 0x34)))

    def test_multiple_packet(self):
        """
        Checks that we can have several packets that will be parsed at once.
        """
        data = bytes((0x42, 0x34, slip.END, 0xde, 0xad, slip.END))
        decoder = slip.decode(data)
        self.assertEqual(next(decoder), bytes((0x42, 0x34)))
        self.assertEqual(next(decoder), bytes((0xde, 0xad)))

    def test_escape_end(self):
        """
        Checks that we can the END is correctly un-escaped.
        """
        data = bytes((slip.ESC, slip.ESC_END, slip.END))
        expected = bytes((slip.END, ))
        decoder = slip.decode(data)
        self.assertEqual(next(decoder), expected)

    def test_escape_escape(self):
        """
        Checks that ESC is correctly un-escaped
        """
        data = bytes((slip.ESC, slip.ESC_ESC, slip.END))
        expected = bytes((slip.ESC, ))
        decoder = slip.decode(data)
        self.assertEqual(next(decoder), expected)

    def test_unsecape_unknown(self):
        """"
        Checks that we raise a ValueError in case of an unknown escape sequence.
        """
        data = bytes((slip.ESC, 0x42, slip.END))

        with self.assertRaises(ValueError):
            next(slip.decode(data))
