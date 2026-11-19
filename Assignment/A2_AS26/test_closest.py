import random
import unittest

from closest import closest_pair, closest_pair_brute


class ClosestPairTests(unittest.TestCase):
    def check_both_methods(self, points):
        expected = closest_pair_brute(points)
        actual = closest_pair(points)
        self.assertAlmostEqual(actual[0], expected[0])
        self.assertEqual(actual[1:], expected[1:])

    def test_examples(self):
        points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
        self.check_both_methods(points)

    def test_exactly_two_points(self):
        self.check_both_methods([(0, 0), (3, 4)])

    def test_duplicate_points(self):
        self.check_both_methods([(1, 1), (5, 5), (1, 1), (8, 2)])

    def test_vertical_line(self):
        self.check_both_methods([(0, 0), (0, 10), (0, 4), (0, 5)])

    def test_pair_across_dividing_line(self):
        self.check_both_methods([(0, 0), (10, 10), (4, 4), (5, 4.1)])

    def test_random_inputs(self):
        random.seed(302)
        for _ in range(500):
            size = random.randint(2, 50)
            points = [(random.randint(-1000, 1000),
                       random.randint(-1000, 1000))
                      for _ in range(size)]
            self.check_both_methods(points)

    def test_too_few_points(self):
        with self.assertRaises(ValueError):
            closest_pair([])
        with self.assertRaises(ValueError):
            closest_pair_brute([(1, 2)])


if __name__ == "__main__":
    unittest.main()

