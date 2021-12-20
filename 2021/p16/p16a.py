import math
import sys


class Packet:
    VERSION_BIT_LENGTH = 3
    TYPE_ID_BIT_LENGTH = 3
    OP_MODE_LENGTH = 1
    LITERAL_TYPE_ID = 4
    HEADER_LEN = VERSION_BIT_LENGTH + TYPE_ID_BIT_LENGTH + OP_MODE_LENGTH

    def __init__(self, version, type_id, value=None, length=0):
        self.version = version
        self.type_id = type_id
        self.value = value
        self.length = length

    def parse_value(self, payload):
        pass


class LiteralPacket(Packet):
    LITERAL_TYPE_ID = 4

    def parse_value(self, payload: str) -> str:
        section_len = 5
        prefix = 1
        shift = 0
        value_bits = ""
        while int(prefix):
            prefix = payload[shift]
            four_bits = payload[shift + 1:shift + section_len]
            value_bits += four_bits
            shift += section_len
        self.value = int(value_bits, 2)
        self.len = shift + Packet.VERSION_BIT_LENGTH + Packet.TYPE_ID_BIT_LENGTH
        return payload[shift:]


class PacketOperator(Packet):
    pass


class OperatorMode0Packet(PacketOperator):
    OP_MODE = "0"
    MODE_SP_INFO_LEN = 15

    def __init__(self, version, type_id, value=None, sub_packets_len=0):
        super().__init__(version, type_id, value)
        self.sub_packets = []
        self.sub_packets_len = sub_packets_len

    def parse_sub_packets_info(self, payload):
        sub_packets_len_bin = payload[:OperatorMode0Packet.MODE_SP_INFO_LEN]
        self.sub_packets_len = int(sub_packets_len_bin, 2)
        return payload[OperatorMode0Packet.MODE_SP_INFO_LEN:]


class OperatorMode1Packet(PacketOperator):
    OP_MODE = "1"
    MODE_SP_INFO_LEN = 11

    def __init__(self, version, type_id, value=None, sub_packets_nb=0):
        super().__init__(version, type_id, value)
        self.sub_packets = []
        self.sub_packets_nb = sub_packets_nb

    def parse_sub_packets_info(self, payload):
        sub_packets_nb_bin = payload[:OperatorMode1Packet.MODE_SP_INFO_LEN]
        self.sub_packets_nb = int(sub_packets_nb_bin, 2)
        return payload[OperatorMode1Packet.MODE_SP_INFO_LEN:]


class PacketFactory:
    @staticmethod
    def make(bin_repr_hdr: str):
        version = int(bin_repr_hdr[:Packet.VERSION_BIT_LENGTH], 2)
        type_id = int(bin_repr_hdr[Packet.VERSION_BIT_LENGTH:Packet.VERSION_BIT_LENGTH + Packet.TYPE_ID_BIT_LENGTH], 2)
        if type_id == LiteralPacket.LITERAL_TYPE_ID:
            return LiteralPacket(version, type_id)
        else:
            op_mode = bin_repr_hdr[Packet.VERSION_BIT_LENGTH + Packet.TYPE_ID_BIT_LENGTH + Packet.OP_MODE_LENGTH - 1]
            if op_mode == OperatorMode0Packet.OP_MODE:
                return OperatorMode0Packet(version, type_id)
            else:
                return OperatorMode1Packet(version, type_id)


def parse_bin_repr(bin_repr: str, packet_nb=math.inf, packet_len=math.inf) -> (int, str, list[Packet]):
    packets = []
    version_sum = 0
    packet_length = 0
    while bin_repr and int(bin_repr) > 0 and len(packets) != packet_nb and packet_length != packet_len:
        print(bin_repr)
        packet = PacketFactory.make(bin_repr[:Packet.HEADER_LEN])
        version_sum += packet.version
        packets.append(packet)
        if packet.__class__ == LiteralPacket:
            # Minus 1 because the header does not hold an OP_MODE
            payload = bin_repr[Packet.HEADER_LEN - 1:]
            bin_repr = packet.parse_value(payload)
            packet_length += packet.len
        else:
            payload = bin_repr[Packet.HEADER_LEN:]
            bin_repr = packet.parse_sub_packets_info(payload)
            if packet.__class__ == OperatorMode0Packet:
                sp_version_sum, bin_repr, sub_packets = parse_bin_repr(bin_repr, packet_len=packet.sub_packets_len)
                packet_length += Packet.HEADER_LEN + OperatorMode0Packet.MODE_SP_INFO_LEN
                packet_length += sum([sp.length for sp in sub_packets])
            else:
                sp_version_sum, bin_repr, sub_packets = parse_bin_repr(bin_repr, packet_nb=packet.sub_packets_nb)
                packet_length += Packet.HEADER_LEN + OperatorMode1Packet.MODE_SP_INFO_LEN
                packet_length += sum([sp.length for sp in sub_packets])
            packet.sub_packets += sub_packets
            version_sum += sp_version_sum

    return version_sum, bin_repr, packets


def parse(filename) -> list[(int, Packet)]:
    with open(filename) as f:
        hex_reprs = f.read().splitlines()

    hex_alphabet_length = 16
    hex_on_bit_length = 4
    bit_prefix_length = 2
    packets = []
    count = 0
    for hex_repr in hex_reprs:
        count += 1
        bin_repr = bin(int(hex_repr, hex_alphabet_length))[bit_prefix_length:]
        bin_repr_len = len(bin_repr)
        bin_repr = bin_repr.zfill(math.ceil(bin_repr_len / hex_on_bit_length) * hex_on_bit_length)
        version_sum, _, packet = parse_bin_repr(bin_repr)
        packets.append((version_sum, packet))
    return packets


def run() -> None:
    if len(sys.argv) != 2:
        print("Missing input file. Run with: python {} [FILENAME].".format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    packets = parse(sys.argv[1])
    for version_sum, _ in packets:
        print(version_sum)


if __name__ == "__main__":
    run()
