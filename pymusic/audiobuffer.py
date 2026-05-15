# Author:  Martin McBride
# Created: 2026-05-14
# Copyright (C) 2026, Martin McBride
# License: MIT

"""
audio_buffer.py

Create a numpy float audio buffer of a given length and write it to a WAV file.

Usage (as a module):
    from audio_buffer import AudioFile
    buf = AudioFile("out.wav", length=2.0)
    buf.sample_buffer[:] = ...        # fill with audio
    buf.write()
"""

import wave
from pathlib import Path
from typing import Union

import numpy as np
import numpy.typing as npt

class AudioBuffer:
    """
    Holds a mono float32 audio buffer and can write it out as a 16-bit WAV file.

    Parameters
    ----------
    length : float or int
        Interpreted as duration in seconds (samples = length * sample_rate)
    sample_rate : int, optional
        Sample rate in Hz (default 44100).
    """

    def __init__(
        self,
        length: Union[float, int],
        sample_rate: int = 44100,
    ):
        if sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if length <= 0:
            raise ValueError("length must be positive")

        self.sample_rate = sample_rate
        self.n_channels = 1 # mono
        self.sampwidth = 2 # 2 bytes, 16 bit

        num_samples = int(round(length * sample_rate)) + 1

        if num_samples <= 0:
            raise ValueError("Computed number of samples must be positive")

        self._samples: np.ndarray = np.zeros(num_samples, dtype=np.float32)

    # ---------- Properties ----------

    @property
    def sample_buffer(self) -> npt.NDArray[np.float32]:
        return self._samples

    @property
    def num_samples(self) -> int:
        return self._samples.shape[0]

    @property
    def duration(self) -> float:
        return self.num_samples / self.sample_rate

    @property
    def sample_rate(self) -> float:
        return self.sample_rate

    # ---------- I/O ----------

    def write(self, filename: Union[str, Path]) -> None:
        """
        Write the buffer to disk as a 16-bit PCM mono WAV file.

        Float samples are clipped to [-1.0, 1.0] and scaled to int16.
        """
        clipped = np.clip(self._samples, -1.0, 1.0)
        int_samples = (clipped * 32767.0).astype(np.int16)

        fn = str(Path(filename).with_suffix(".wav"))

        with wave.open(fn, "wb") as wf:
            wf.setnchannels(self.n_channels)
            wf.setsampwidth(self.sampwidth)
            wf.setframerate(self.sample_rate)
            wf.writeframes(int_samples.tobytes())

    def __repr__(self) -> str:
        return (
            f"num_samples={self.num_samples}, "
            f"sample_rate={self.sample_rate})"
        )

def read_wav(filename: Union[str, Path]) -> AudioBuffer:
    fn = str(Path(filename).with_suffix(".wav"))
    with wave.open(fn, "rb") as wf:
        sample_rate = wf.getframerate()
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        n_frames = wf.getnframes()

        if sampwidth != 2:
            raise ValueError("Reading {fn} - sample width must be 2")

        if n_channels != 1:
            raise ValueError("Reading {fn} - number of channels must be 1")

        # Read raw bytes
        dtype_map = {1: np.uint8, 2: np.int16, 4: np.int32}
        audioBuffer = AudioBuffer(n_frames, sample_rate)
        audioBuffer.sample_buffer = np.frombuffer(wf.readframes(n_frames), dtype=dtype_map[sampwidth])

        return audioBuffer

