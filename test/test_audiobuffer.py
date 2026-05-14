# Author:  Martin McBride
# Created: 2026-05-14
# Copyright (C) 2026, Martin McBride
# License: MIT

"""
test_audio_buffer.py

Unit tests for audio_buffer.AudioFile.
"""

import os
import tempfile
import unittest
import wave
from pathlib import Path

import numpy as np

from pymusic.audiobuffer import AudioBuffer


class TestAudioFileConstruction(unittest.TestCase):
    def test_default_sample_rate(self):
        buf = AudioBuffer(length=1.0)
        self.assertEqual(buf.sample_rate, 44100)

    def test_custom_sample_rate(self):
        buf = AudioBuffer(length=1.0, sample_rate=48000)
        self.assertEqual(buf.sample_rate, 48000)

    def test_num_samples_from_float_length(self):
        # Implementation uses: round(length * sample_rate) + 1
        buf = AudioBuffer(length=1.0, sample_rate=44100)
        self.assertEqual(buf.num_samples, 44101)

    def test_num_samples_from_fractional_length(self):
        buf = AudioBuffer(length=0.5, sample_rate=44100)
        self.assertEqual(buf.num_samples, int(round(0.5 * 44100)) + 1)

    def test_num_samples_from_int_length(self):
        # Integer length is still treated as seconds (length * sample_rate)
        buf = AudioBuffer(length=2, sample_rate=1000)
        self.assertEqual(buf.num_samples, 2001)

    def test_duration_property(self):
        sr = 44100
        buf = AudioBuffer(length=1.0, sample_rate=sr)
        # duration = num_samples / sample_rate = 44101 / 44100
        self.assertAlmostEqual(buf.duration, 44101 / sr)

    # ---------- Error cases ----------

    def test_zero_length_raises(self):
        with self.assertRaises(ValueError):
            AudioBuffer(length=0)

    def test_negative_length_raises(self):
        with self.assertRaises(ValueError):
            AudioBuffer(length=-1.0)

    def test_zero_sample_rate_raises(self):
        with self.assertRaises(ValueError):
            AudioBuffer(length=1.0, sample_rate=0)

    def test_negative_sample_rate_raises(self):
        with self.assertRaises(ValueError):
            AudioBuffer(length=1.0, sample_rate=-44100)


class TestAudioFileSamples(unittest.TestCase):
    def test_samples_initialized_to_zero(self):
        buf = AudioBuffer(length=1.0)
        self.assertTrue(np.all(buf.sample_buffer == 0.0))

    def test_samples_dtype_float32(self):
        buf = AudioBuffer(length=1.0)
        self.assertEqual(buf.sample_buffer.dtype, np.float32)

    def test_samples_shape_matches_num_samples(self):
        buf = AudioBuffer(length=1.0, sample_rate=1000)
        self.assertEqual(buf.sample_buffer.shape, (buf.num_samples,))

    def test_sample_buffer_is_mutable(self):
        buf = AudioBuffer(length=1.0, sample_rate=1000)
        buf.sample_buffer[0] = 0.5
        self.assertEqual(buf.sample_buffer[0], np.float32(0.5))

    def test_sample_buffer_returns_same_array(self):
        # Property should expose the underlying array (not a copy),
        # so in-place edits persist.
        buf = AudioBuffer(length=1.0, sample_rate=1000)
        a = buf.sample_buffer
        a[:] = 0.25
        self.assertTrue(np.all(buf.sample_buffer == np.float32(0.25)))


class TestAudioFileRepr(unittest.TestCase):
    def test_repr_contains_fields(self):
        buf = AudioBuffer(length=1.0, sample_rate=22050)
        r = repr(buf)
        self.assertIn("sample_rate=22050", r)
        self.assertIn(f"num_samples={buf.num_samples}", r)


class TestAudioFileWrite(unittest.TestCase):
    """
    Tests for AudioFile.write().

    NOTE: The current implementation of `write()` references `self.samples`,
    but the class exposes the buffer via `self._samples` / `self.sample_buffer`.
    These tests will therefore fail with AttributeError until `write()` is
    fixed to use `self._samples` (or `self.sample_buffer`). The tests are
    written against the *intended* behavior.
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        for name in os.listdir(self.tmpdir):
            try:
                os.remove(os.path.join(self.tmpdir, name))
            except OSError:
                pass
        os.rmdir(self.tmpdir)

    def _path(self, name: str) -> str:
        return os.path.join(self.tmpdir, name)

    def test_write_creates_file(self):
        path = self._path("out.wav")
        buf = AudioBuffer(length=0.1, sample_rate=8000)
        buf.write(path)
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_write_produces_valid_wav_header(self):
        path = self._path("out.wav")
        sr = 8000
        buf = AudioBuffer(length=0.1, sample_rate=sr)
        buf.write(path)

        with wave.open(path, "rb") as wf:
            self.assertEqual(wf.getnchannels(), 1)   # mono
            self.assertEqual(wf.getsampwidth(), 2)   # 16-bit
            self.assertEqual(wf.getframerate(), sr)
            self.assertEqual(wf.getnframes(), buf.num_samples)

    def test_write_silence_produces_zero_samples(self):
        path = self._path("silence.wav")
        buf = AudioBuffer(length=0.05, sample_rate=8000)
        buf.write(path)

        with wave.open(path, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)
        self.assertTrue(np.all(data == 0))
        self.assertEqual(len(data), buf.num_samples)

    def test_write_scales_float_to_int16(self):
        path = self._path("tone.wav")
        sr = 8000
        buf = AudioBuffer(length=0.01, sample_rate=sr)
        # Fill with a known constant value
        buf.sample_buffer[:] = 0.5
        buf.write(path)

        with wave.open(path, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)
        expected = np.int16(np.floor(0.5 * 32767.0))
        self.assertTrue(np.all(data == expected))

    def test_write_clips_values_above_one(self):
        path = self._path("clip_high.wav")
        buf = AudioBuffer(length=0.01, sample_rate=8000)
        buf.sample_buffer[:] = 2.0  # out of range
        buf.write(path)

        with wave.open(path, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)
        # Clipped to 1.0, scaled to 32767
        self.assertTrue(np.all(data == 32767))

    def test_write_clips_values_below_minus_one(self):
        path = self._path("clip_low.wav")
        buf = AudioBuffer(length=0.01, sample_rate=8000)
        buf.sample_buffer[:] = -2.0  # out of range
        buf.write(path)

        with wave.open(path, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
        data = np.frombuffer(frames, dtype=np.int16)
        # Clipped to -1.0, scaled to -32767
        self.assertTrue(np.all(data == -32767))

    def test_write_roundtrip_sine(self):
        path = self._path("sine.wav")
        sr = 8000
        buf = AudioBuffer(length=0.05, sample_rate=sr)
        t = np.arange(buf.num_samples) / sr
        buf.sample_buffer[:] = (0.5 * np.sin(2 * np.pi * 440.0 * t)).astype(np.float32)
        buf.write(path)

        with wave.open(path, "rb") as wf:
            self.assertEqual(wf.getframerate(), sr)
            self.assertEqual(wf.getnframes(), buf.num_samples)
            frames = wf.readframes(wf.getnframes())

        data = np.frombuffer(frames, dtype=np.int16)
        # Reconstruct float approximation and compare with loose tolerance
        reconstructed = data.astype(np.float32) / 32767.0
        np.testing.assert_allclose(reconstructed, buf.sample_buffer, atol=1e-3)


if __name__ == "__main__":
    unittest.main()