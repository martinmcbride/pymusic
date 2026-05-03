from dataclasses import dataclass, field
from typing import Tuple


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
