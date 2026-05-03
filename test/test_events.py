import unittest
from dataclasses import is_dataclass

from pymusic.events import Event  # assumes the Event class is in event.py


class TestEvent(unittest.TestCase):
    # ---------- Construction ----------

    def test_is_dataclass(self):
        self.assertTrue(is_dataclass(Event))

    def test_basic_construction_no_extras(self):
        e = Event(0.0, 1.5, 60, 0.8)
        self.assertEqual(e.start, 0.0)
        self.assertEqual(e.duration, 1.5)
        self.assertEqual(e.pitch, 60)
        self.assertEqual(e.volume, 0.8)
        self.assertEqual(e.extras, ())

    def test_construction_with_single_extra(self):
        e = Event(0.0, 1.0, 60, 0.5, 0.1)
        self.assertEqual(e.extras, (0.1,))

    def test_construction_with_multiple_extras(self):
        e = Event(0.0, 1.0, 60, 0.5, 0.1, 0.2, 0.3)
        self.assertEqual(e.extras, (0.1, 0.2, 0.3))

    def test_extras_is_tuple(self):
        e = Event(0.0, 1.0, 60, 0.5, 1, 2, 3)
        self.assertIsInstance(e.extras, tuple)

    def test_keyword_arguments(self):
        e = Event(start=1.0, duration=2.0, pitch=64, volume=0.9)
        self.assertEqual(e.start, 1.0)
        self.assertEqual(e.duration, 2.0)
        self.assertEqual(e.pitch, 64)
        self.assertEqual(e.volume, 0.9)
        self.assertEqual(e.extras, ())

    # ---------- Error cases ----------

    def test_missing_required_arguments_raises(self):
        with self.assertRaises(TypeError):
            Event(0.0, 1.0, 60)  # missing volume

    def test_no_arguments_raises(self):
        with self.assertRaises(TypeError):
            Event()

    # ---------- Numeric types ----------

    def test_integer_values(self):
        e = Event(0, 1, 60, 1, 2, 3)
        self.assertEqual(e.start, 0)
        self.assertEqual(e.duration, 1)
        self.assertEqual(e.pitch, 60)
        self.assertEqual(e.volume, 1)
        self.assertEqual(e.extras, (2, 3))

    def test_float_values(self):
        e = Event(0.25, 0.5, 60.5, 0.75, 1.5, 2.5)
        self.assertAlmostEqual(e.start, 0.25)
        self.assertAlmostEqual(e.duration, 0.5)
        self.assertAlmostEqual(e.pitch, 60.5)
        self.assertAlmostEqual(e.volume, 0.75)
        self.assertEqual(e.extras, (1.5, 2.5))

    def test_negative_values_allowed(self):
        # No validation is enforced, so negatives should be accepted
        e = Event(-1.0, -2.0, -60, -0.5, -1, -2)
        self.assertEqual(e.start, -1.0)
        self.assertEqual(e.duration, -2.0)
        self.assertEqual(e.pitch, -60)
        self.assertEqual(e.volume, -0.5)
        self.assertEqual(e.extras, (-1, -2))

    def test_zero_values(self):
        e = Event(0, 0, 0, 0)
        self.assertEqual((e.start, e.duration, e.pitch, e.volume), (0, 0, 0, 0))
        self.assertEqual(e.extras, ())

    # ---------- Equality & repr ----------

    def test_equality_same_values(self):
        a = Event(0.0, 1.0, 60, 0.8, 0.1, 0.2)
        b = Event(0.0, 1.0, 60, 0.8, 0.1, 0.2)
        self.assertEqual(a, b)

    def test_equality_different_extras(self):
        a = Event(0.0, 1.0, 60, 0.8, 0.1)
        b = Event(0.0, 1.0, 60, 0.8, 0.2)
        self.assertNotEqual(a, b)

    def test_equality_different_core_fields(self):
        a = Event(0.0, 1.0, 60, 0.8)
        b = Event(0.0, 1.0, 61, 0.8)
        self.assertNotEqual(a, b)

    def test_equality_extras_length_differs(self):
        a = Event(0.0, 1.0, 60, 0.8, 0.1)
        b = Event(0.0, 1.0, 60, 0.8, 0.1, 0.2)
        self.assertNotEqual(a, b)

    def test_repr_contains_all_fields(self):
        e = Event(0.0, 1.0, 60, 0.8, 0.1, 0.2)
        r = repr(e)
        self.assertIn("Event", r)
        self.assertIn("start=0.0", r)
        self.assertIn("duration=1.0", r)
        self.assertIn("pitch=60", r)
        self.assertIn("volume=0.8", r)
        self.assertIn("extras=(0.1, 0.2)", r)

    # ---------- Mutation ----------

    def test_fields_are_mutable(self):
        e = Event(0.0, 1.0, 60, 0.8)
        e.start = 5.0
        e.pitch = 72
        self.assertEqual(e.start, 5.0)
        self.assertEqual(e.pitch, 72)

    def test_extras_tuple_is_immutable(self):
        e = Event(0.0, 1.0, 60, 0.8, 0.1, 0.2)
        with self.assertRaises(TypeError):
            e.extras[0] = 9.9  # tuples don't support item assignment

    # ---------- Unpacking scenarios ----------

    def test_construction_from_unpacked_sequence(self):
        data = (0.0, 1.0, 60, 0.8, 0.1, 0.2, 0.3)
        e = Event(*data)
        self.assertEqual(e.start, 0.0)
        self.assertEqual(e.extras, (0.1, 0.2, 0.3))

    def test_large_number_of_extras(self):
        extras = tuple(range(100))
        e = Event(0, 1, 60, 0.5, *extras)
        self.assertEqual(e.extras, extras)
        self.assertEqual(len(e.extras), 100)


if __name__ == "__main__":
    unittest.main()