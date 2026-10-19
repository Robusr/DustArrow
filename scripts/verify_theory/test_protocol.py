import re
import struct
import unittest


ARCHIVED_PATTERN = re.compile(r"X(.+)Y(.+)GX(.+)GY(.+)GZ(.+)")


def parse_archived(stream):
    match = ARCHIVED_PATTERN.search(stream)
    return match.groups() if match else None


def crc16_ccitt_false(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def encode_frame(payload):
    if len(payload) > 255:
        raise ValueError("payload too long for one-byte length")
    body = bytes([len(payload)]) + payload
    return b"$" + body + struct.pack(">H", crc16_ccitt_false(body)) + b"*"


class FrameParser:
    def __init__(self):
        self.buffer = bytearray()

    def feed(self, chunk):
        self.buffer.extend(chunk)
        frames = []
        while True:
            start = self.buffer.find(b"$")
            if start < 0:
                self.buffer.clear()
                break
            if start > 0:
                del self.buffer[:start]
            if len(self.buffer) < 2:
                break
            length = self.buffer[1]
            total = 1 + 1 + length + 2 + 1
            if len(self.buffer) < total:
                break
            payload = bytes(self.buffer[2 : 2 + length])
            received = struct.unpack(">H", bytes(self.buffer[2 + length : 4 + length]))[0]
            terminator = self.buffer[4 + length]
            body = bytes(self.buffer[1 : 2 + length])
            if terminator == ord("*") and crc16_ccitt_false(body) == received:
                frames.append(payload)
                del self.buffer[:total]
            else:
                del self.buffer[:1]
        return frames


class ArchivedProtocolTests(unittest.TestCase):
    def test_full_text_frame_parses(self):
        groups = parse_archived("X10.0Y20.0GX1.0GY2.0GZ3.0")
        self.assertEqual(groups, ("10.0", "20.0", "1.0", "2.0", "3.0"))

    def test_split_frame_is_lost(self):
        first, second = "X10.0Y2", "0.0GX1.0GY2.0GZ3.0"
        self.assertIsNone(parse_archived(first))
        self.assertIsNone(parse_archived(second))

    def test_greedy_regex_misparses_concatenated_frames(self):
        groups = parse_archived("X1Y2GX3GY4GZ5X6Y7GX8GY9GZ10")
        self.assertNotEqual(groups, ("1", "2", "3", "4", "5"))
        self.assertIn("GZ", groups[0])


class ProposedFrameTests(unittest.TestCase):
    def payload(self, n=1):
        return struct.pack("<I5f", 1234 + n, 10.0 * n, -20.0 * n, 1.0, 2.0, 3.0)

    def test_roundtrip(self):
        payload = self.payload()
        parser = FrameParser()
        self.assertEqual(parser.feed(encode_frame(payload)), [payload])

    def test_byte_by_byte_reassembly(self):
        payload = self.payload(2)
        frame = encode_frame(payload)
        parser = FrameParser()
        out = []
        for byte in frame:
            out.extend(parser.feed(bytes([byte])))
        self.assertEqual(out, [payload])

    def test_noise_before_header_is_ignored(self):
        payload = self.payload(3)
        parser = FrameParser()
        self.assertEqual(parser.feed(b"\x00\xffnoise" + encode_frame(payload)), [payload])

    def test_bad_crc_is_rejected(self):
        frame = bytearray(encode_frame(self.payload(4)))
        frame[-2] ^= 0xFF
        parser = FrameParser()
        self.assertEqual(parser.feed(bytes(frame)), [])

    def test_two_frames_in_one_chunk(self):
        p1, p2 = self.payload(5), self.payload(6)
        parser = FrameParser()
        self.assertEqual(parser.feed(encode_frame(p1) + encode_frame(p2)), [p1, p2])

    def test_crc_known_vector(self):
        # CRC-16/CCITT-FALSE of the ASCII string "123456789" is 0x29B1.
        self.assertEqual(crc16_ccitt_false(b"123456789"), 0x29B1)


if __name__ == "__main__":
    unittest.main()
