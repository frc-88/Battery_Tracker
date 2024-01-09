from __future__ import annotations

import struct

from dslogs.entry.pdp_data import PdpData


def reverse_endian(value: int, int_size: int) -> int:
    return int.from_bytes(value.to_bytes(int_size, byteorder="big"), byteorder="little")


class PdpRevPdhData(PdpData):
    byte_code = ">B" + ("I" * 6) + ("B" * 3) + ("B" * 5)

    def __init__(self, pdp_id: int, currents: list[float], temperature: float) -> None:
        self.pdp_id = pdp_id
        self.currents = currents
        self.voltage = 0.0
        self.resistance = 0.0
        self.temperature = temperature

    @classmethod
    def from_bytes(cls, data: bytes) -> PdpRevPdhData:
        parsed = struct.unpack(cls.byte_code, data)
        pdp_id = data[0]
        ints = []
        for i in range(1, 7):
            ints.append(reverse_endian(parsed[i], 4))
        ints[6] = int.from_bytes(
            b"".join([i.to_bytes(1, "big") for i in parsed[7:10]]) + b"\x00",
            byteorder="big",
        )

        currents = [0.0 for _ in range(24)]
        for index in range(len(currents)):
            data_index = index // 3
            data_offset = index % 3
            value = ints[data_index]
            voltage = value << (32 - ((data_offset + 1) * 10))
            voltage = voltage >> 22
            currents[index] = voltage / 8
        for index in range(4):
            currents[index + 20] = parsed[index + 10] / 16
        temperature = parsed[14]

        return cls(pdp_id, currents, temperature)

    @classmethod
    def length(cls) -> int:
        return struct.calcsize(cls.byte_code)
