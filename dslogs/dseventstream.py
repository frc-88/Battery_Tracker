from io import TextIOWrapper
from typing import Generator, Optional
from dslogs.entry.metadata import Metadata
from dslogs.entry.event_entry import EventEntry


class DsEventStream:
    def __init__(self, file: TextIOWrapper) -> None:
        self.file = file
        self.metadata = Metadata.from_bytes(self.file.read(Metadata.length()))
        if self.metadata.version != 4:
            raise ValueError(f"Unsupported log version {self.metadata.version}")

    def __iter__(self) -> Generator[EventEntry, None, None]:
        self.start_time = self.metadata.date
        while True:
            if data := self.conditional_read(EventEntry.length()):
                entry = EventEntry.from_bytes(data)
            else:
                break
            if data := self.conditional_read(entry.message_length):
                entry.parse_message(data)
            else:
                break
            yield entry

    def conditional_read(self, expected_size: int) -> Optional[bytes]:
        data = self.file.read(expected_size)
        if len(data) != expected_size:
            return None
        return data
