#!/usr/bin/env python3

import context
import unittest
import local_directional_pattern as LDP

class TestLDP(unittest.TestCase):

	def test_histogram(self):
		m1 = [
			[1, 2, 5],
			[4, 5, 7],
			[2, 6, 0],
			[3, 1, 4]
		]
		histogram_size = 8
		histogram = LDP.histogramize(m1, histogram_size)
		self.assertEqual(histogram, [1, 2, 2, 1, 2, 2, 1, 1])

if __name__ == '__main__':
	unittest.main()