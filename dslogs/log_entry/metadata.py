from __future__ import annotations
import struct
from datetime import datetime, timedelta
from pytz import timezone
from dslogs.log_entry.generic_entry import GenericEntry

UINT64_MAX = (1 << 64) - 1


class Metadata(GenericEntry):
    byte_code = ">iqQ"

    def __init__(self, version: int, unix_time: float, offset: int):
        self.version = version
        self.unix_time = unix_time
        self.offset = offset

    @classmethod
    def from_bytes(cls, data: bytes) -> Metadata:
        version, unix_time, offset = struct.unpack(cls.byte_code, data)
        return cls(version, unix_time, offset)

    @classmethod
    def length(cls) -> int:
        return struct.calcsize(cls.byte_code)

    @property
    def date(self) -> datetime:
        epoch = datetime(1904, 1, 1, 0, 0, 0, 0, timezone("UTC"))
        date = epoch + timedelta(seconds=self.unix_time)
        date += timedelta(seconds=self.offset / UINT64_MAX)
        return date
