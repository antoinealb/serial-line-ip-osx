import unittest
import slip
import io

class SLIPDecoderTestCase(unittest.TestCase):
    def test_end_marker(self):
        """
        Check that the packets are delimited by the end marker.
        """
        data = bytes((0x42, 0x34)) + slip.END
        data = io.BytesIO(data)
        self.assertEqual(next(slip.decode(data)), bytes((0x42, 0x34)))

    def test_multiple_packet(self):
        """
        Checks that we can have several packets that will be parsed at once.
        """
        data = bytes((0x42, 0x34)) + slip.END + bytes((0xde, 0xad)) + slip.END
        data = io.BytesIO(data)
        decoder = slip.decode(data)
        self.assertEqual(next(decoder), bytes((0x42, 0x34)))
        self.assertEqual(next(decoder), bytes((0xde, 0xad)))

    def test_escape_end(self):
        """
        Checks that we can the END is correctly un-escaped.
        """
        data = slip.ESC + slip.ESC_END + slip.END
        data = io.BytesIO(data)

        expected = slip.END

        decoder = slip.decode(data)
        self.assertEqual(next(decoder), expected)

    def test_escape_escape(self):
        """
        Checks that ESC is correctly un-escaped
        """
        data = slip.ESC + slip.ESC_ESC + slip.END
        data = io.BytesIO(data)

        expected = slip.ESC

        decoder = slip.decode(data)
        self.assertEqual(next(decoder), expected)

    def test_unescape_unknown(self):
        """"
        Checks that we raise a ValueError in case of an unknown escape sequence.
        """
        data = slip.ESC + bytes((0x42, )) + slip.END
        data = io.BytesIO(data)

        with self.assertRaises(ValueError):
            next(slip.decode(data))
