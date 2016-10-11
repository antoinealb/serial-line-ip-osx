from hypothesis import given
from hypothesis import strategies as st
import unittest
import io

from slip import *

class SLIPEncodeTestCase(unittest.TestCase):
    def test_append_end(self):
        """
        Checks that the end char is appended.
        """
        data = bytes((0x42, ))
        data = encode(data)
        expected = bytes((0x42, END))
        self.assertEqual(data, expected)

    def test_end_is_escaped(self):
        """
        Checks that END is correctly escaped.
        """
        data = bytes((END, ))
        data = encode(data)
        expected = bytes((ESC, ESC_END, END))

        self.assertEqual(expected, data, "END is not correctly escaped")

    def test_esc_is_escaped(self):
        """
        Checks that ESC is correctly escaped.
        """
        data = bytes((ESC, ))
        data = encode(data)
        expected = bytes((ESC, ESC_ESC, END))

        self.assertEqual(expected, data, "ESC is not correctly escaped")


class EndToEndTestCase(unittest.TestCase):
    @given(st.binary())
    def test_encode_then_decode(self, data):
        encoded = encode(data)
        decoded = next(decode(io.BytesIO(encoded)))
        assert data == decoded
