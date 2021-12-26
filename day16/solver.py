from utils.parsers import parse_line
from utils.slide_iter import SlideIter


text_bytes = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

class Transmission(object):

    def __init__(self):
        self.raw_transmission = parse_line("day16/input.txt")
        self.transmission = "".join((text_bytes[c] for c in self.raw_transmission))

    def getBitIter(self, offset=0):
        return SlideIter(self.transmission, offset)


class Packet(object):

    def __init__(self, bit_iter):
        self.raw_version = bit_iter.get(3)
        self.version = int(self.raw_version, 2)
        self.raw_type_id = bit_iter.get(3)
        self.type_id = int(self.raw_type_id, 2)

    packet_types = {}

    @classmethod
    def constructPacket(cls, bit_iter):
        type_id = int(bit_iter.peek_from(3, 3), 2)
        packet_type = cls.packet_types.get(type_id, None)
        if packet_type:
            return packet_type(bit_iter)
        return cls.packet_types[0](bit_iter)


class LiteralPacket(Packet):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        bit_chunks = []
        while bit_iter.get(1) != '0':
            bit_chunks.append(bit_iter.get(4))
        bit_chunks.append(bit_iter.get(4))
        self.value = int("".join(bit_chunks), 2)

    def __rep__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class OperatorPacket(Packet):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        self.length_type_id = bit_iter.get(1)
        if '0' == self.length_type_id:
            # Total length in bits of sub packets
            self.raw_length = bit_iter.get(15)
            self.length = int(self.raw_length, 2)
            self.sub_packets = []
            start_offset = bit_iter.offset
            while bit_iter.offset - start_offset != self.length:
                self.sub_packets.append(Packet.constructPacket(bit_iter))
        else:
            self.raw_length = bit_iter.get(11)
            self.length = int(self.raw_length, 2)
            self.sub_packets = [Packet.constructPacket(bit_iter) for _ in range(self.length)]


class SumPacket(OperatorPacket):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        self.value = 0
        for sub_packet in self.sub_packets:
            self.value += sub_packet.value


class ProductPacket(OperatorPacket):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        self.value = 1
        for sub_packet in self.sub_packets:
            self.value *= sub_packet.value


class MinimumPacket(OperatorPacket):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        self.value = self.sub_packets[0].value
        for sub_packet in self.sub_packets:
            self.value = min(self.value, sub_packet.value)


class MaximumPacket(OperatorPacket):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        self.value = self.sub_packets[0].value
        for sub_packet in self.sub_packets:
            self.value = max(self.value, sub_packet.value)


class GreaterThanPacket(OperatorPacket):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        self.value = 1 if self.sub_packets[0].value > self.sub_packets[1].value else 0


class LessThanPacket(OperatorPacket):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        self.value = 1 if self.sub_packets[0].value < self.sub_packets[1].value else 0


class EqualToPacket(OperatorPacket):

    def __init__(self, bit_iter):
        super().__init__(bit_iter)
        self.value = 1 if self.sub_packets[0].value == self.sub_packets[1].value else 0


Packet.packet_types = {
    0: SumPacket,
    1: ProductPacket,
    2: MinimumPacket,
    3: MaximumPacket,
    4: LiteralPacket,
    5: GreaterThanPacket,
    6: LessThanPacket,
    7: EqualToPacket,
}


def count_versions(packet):
    version_total = packet.version
    if hasattr(packet, "sub_packets"):
        for packet in packet.sub_packets:
            version_total += count_versions(packet)
    return version_total


def solve1():
    print(count_versions(Packet.constructPacket(Transmission().getBitIter())))

def solve2():
    print(Packet.constructPacket(Transmission().getBitIter()).value)
