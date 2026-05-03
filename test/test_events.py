import unittest
from dataclasses import is_dataclass

from pymusic.events import Event, Events


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



class TestEvents(unittest.TestCase):
    # ---------- Construction ----------

    def test_default_construction_empty(self):
        es = Events()
        self.assertEqual(len(es), 0)

    def test_construction_from_list(self):
        data = [Event(0, 1, 60, 0.8), Event(1, 1, 62, 0.7)]
        es = Events(data)
        self.assertEqual(len(es), 2)
        self.assertEqual(es[0], data[0])
        self.assertEqual(es[1], data[1])

    def test_construction_copies_list(self):
        # Mutating the original list should not affect the Events container
        data = [Event(0, 1, 60, 0.8)]
        es = Events(data)
        data.append(Event(1, 1, 62, 0.7))
        self.assertEqual(len(es), 1)

    # ---------- add ----------

    def test_add_single_event(self):
        es = Events()
        e = Event(0, 1, 60, 0.8)
        es.add(e)
        self.assertEqual(len(es), 1)
        self.assertIs(es[0], e)

    def test_add_multiple_events(self):
        es = Events()
        for i in range(5):
            es.add(Event(i, 1, 60 + i, 0.5))
        self.assertEqual(len(es), 5)
        self.assertEqual(es[2].pitch, 62)

    def test_add_non_event_raises(self):
        es = Events()
        with self.assertRaises(TypeError):
            es.add("not an event")
        with self.assertRaises(TypeError):
            es.add((0, 1, 60, 0.8))
        with self.assertRaises(TypeError):
            es.add(None)

    def test_add_preserves_order(self):
        es = Events()
        a = Event(0, 1, 60, 0.8)
        b = Event(1, 1, 62, 0.7)
        c = Event(2, 1, 64, 0.9)
        es.add(a)
        es.add(b)
        es.add(c)
        self.assertEqual(list(es), [a, b, c])

    # ---------- Indexing ----------

    def test_integer_indexing(self):
        a = Event(0, 1, 60, 0.8)
        b = Event(1, 1, 62, 0.7)
        es = Events([a, b])
        self.assertEqual(es[0], a)
        self.assertEqual(es[1], b)

    def test_negative_indexing(self):
        a = Event(0, 1, 60, 0.8)
        b = Event(1, 1, 62, 0.7)
        es = Events([a, b])
        self.assertEqual(es[-1], b)
        self.assertEqual(es[-2], a)

    def test_slice_indexing(self):
        items = [Event(i, 1, 60 + i, 0.5) for i in range(5)]
        es = Events(items)
        self.assertEqual(es[1:4], items[1:4])
        self.assertEqual(es[::2], items[::2])
        self.assertEqual(es[::-1], items[::-1])

    def test_out_of_range_indexing_raises(self):
        es = Events([Event(0, 1, 60, 0.8)])
        with self.assertRaises(IndexError):
            _ = es[5]
        with self.assertRaises(IndexError):
            _ = es[-2]

    # ---------- Iteration ----------

    def test_iteration_yields_all_events(self):
        items = [Event(i, 1, 60 + i, 0.5) for i in range(3)]
        es = Events(items)
        self.assertEqual(list(es), items)

    def test_iteration_multiple_times(self):
        # An iterable (vs. iterator) should be re-iterable
        items = [Event(i, 1, 60 + i, 0.5) for i in range(3)]
        es = Events(items)
        first_pass = list(es)
        second_pass = list(es)
        self.assertEqual(first_pass, second_pass)
        self.assertEqual(first_pass, items)

    def test_iteration_empty(self):
        es = Events()
        self.assertEqual(list(es), [])

    def test_for_loop(self):
        items = [Event(i, 1, 60 + i, 0.5) for i in range(3)]
        es = Events(items)
        collected = []
        for e in es:
            collected.append(e)
        self.assertEqual(collected, items)

    def test_comprehension(self):
        items = [Event(i, 1, 60 + i, 0.5) for i in range(4)]
        es = Events(items)
        pitches = [e.pitch for e in es]
        self.assertEqual(pitches, [60, 61, 62, 63])

    # ---------- Length & truthiness ----------

    def test_len_changes_with_add(self):
        es = Events()
        self.assertEqual(len(es), 0)
        es.add(Event(0, 1, 60, 0.8))
        self.assertEqual(len(es), 1)
        es.add(Event(1, 1, 62, 0.7))
        self.assertEqual(len(es), 2)

    def test_truthiness(self):
        self.assertFalse(bool(Events()))
        self.assertTrue(bool(Events([Event(0, 1, 60, 0.8)])))

    # ---------- Equality & repr ----------

    def test_equality_same_contents(self):
        a = Events([Event(0, 1, 60, 0.8), Event(1, 1, 62, 0.7)])
        b = Events([Event(0, 1, 60, 0.8), Event(1, 1, 62, 0.7)])
        self.assertEqual(a, b)

    def test_equality_different_contents(self):
        a = Events([Event(0, 1, 60, 0.8)])
        b = Events([Event(0, 1, 61, 0.8)])
        self.assertNotEqual(a, b)

    def test_equality_different_lengths(self):
        a = Events([Event(0, 1, 60, 0.8)])
        b = Events([Event(0, 1, 60, 0.8), Event(1, 1, 62, 0.7)])
        self.assertNotEqual(a, b)

    def test_equality_with_non_events(self):
        es = Events([Event(0, 1, 60, 0.8)])
        self.assertNotEqual(es, [Event(0, 1, 60, 0.8)])
        self.assertNotEqual(es, "Events")

    def test_repr_contains_class_name(self):
        es = Events([Event(0, 1, 60, 0.8)])
        self.assertIn("Events", repr(es))
        self.assertIn("Event", repr(es))

    # ---------- Interaction with tuple() / record() ----------

    def test_tuple_conversion(self):
        items = [Event(i, 1, 60 + i, 0.5) for i in range(3)]
        es = Events(items)
        t = tuple(es)
        self.assertIsInstance(t, tuple)
        self.assertEqual(t, tuple(items))


if __name__ == "__main__":
    unittest.main()