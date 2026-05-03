from dataclasses import dataclass, field
from typing import Tuple, Iterator, List, Union, overload


@dataclass
class Event:
    start: float
    duration: float
    pitch: float
    volume: float
    extras: Tuple[float, ...] = field(default_factory=tuple)

    def __init__(
        self,
        start: float,
        duration: float,
        pitch: float,
        volume: float,
        *extras: float,
    ):
        self.start = start
        self.duration = duration
        self.pitch = pitch
        self.volume = volume
        self.extras = extras



class Events:
    """
    A container for a list of Event objects.

    Supports iteration, indexing (including slices), length queries,
    and adding new Events.
    """

    def __init__(self, events: List[Event] = None):
        self._events: List[Event] = list(events) if events is not None else []

    # ---------- Adding ----------

    def add(self, event: Event) -> None:
        """Append a new Event to the collection."""
        if not isinstance(event, Event):
            raise TypeError(f"Expected Event, got {type(event).__name__}")
        self._events.append(event)

    # ---------- Iteration ----------

    def __iter__(self) -> Iterator[Event]:
        return iter(self._events)

    # ---------- Indexing ----------

    def __getitem__(self, index: Union[int, slice]) -> Union[Event, List[Event]]:
        return self._events[index]

    # ---------- Sizing ----------

    def __len__(self) -> int:
        return len(self._events)

    # ---------- Representation ----------

    def __repr__(self) -> str:
        return f"Events({self._events!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Events):
            return NotImplemented
        return self._events == other._events
