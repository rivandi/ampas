#!/usr/bin/env python3

import context
import mathlib
import unittest

class TestMathlib(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestMathlib, self).__init__(*args, **kwargs)
		self.m1 = [
			[1, 2, 3],
			[4, 5, 6],
			[7, 8, 9],
			[10,11,12]
		]
		self.m2 = [[0,1,2,3]]
		self.m3 = [[0],[1],[2],[3]]

	def test_demlo(self):
		d = mathlib.demlo_num(4)
		self.assertEqual(d, 1234321)

		d = mathlib.demlo_num(0)
		self.assertEqual(d, 0)

		d = mathlib.demlo_num(0.5)
		self.assertEqual(d, 0)

	def test_binet(self):
		d = mathlib.binet_fib(50)
		self.assertEqual(d, 12586269025)

		d = mathlib.binet_fib(0)
		self.assertEqual(d, 0)

	def test_divide_matrix_zero(self):
		m = mathlib.divide(self.m1, region=(2,2), zero_mode=True)
		self.assertEqual(m, [[[1, 2], [4, 5]], [[3, 0], [6, 0]], [[7, 8], [10, 11]], [[9, 0], [12, 0]]])

		m = mathlib.divide(self.m2, region=(2,2), zero_mode=True)
		self.assertEqual(m, [[[0, 1]], [[2, 3]], [[0, 0]], [[0, 0]]])

		m = mathlib.divide(self.m3, region=(2,2), zero_mode=True)
		self.assertEqual(m, [[[0], [1]], [[0], [0]], [[2], [3]], [[0], [0]]])

	def test_divide_matrix_nonzero(self):
		m = mathlib.divide(self.m1, region=(2,2), zero_mode=False)
		self.assertEqual(m, [[[1, 2], [4, 5]], [[3], [6]], [[7, 8], [10, 11]], [[9], [12]]])

		m = mathlib.divide(self.m2, region=(2,2), zero_mode=False)
		self.assertEqual(m, [[[0, 1]], [[2, 3]], [], []])

		m = mathlib.divide(self.m3, region=(2,2), zero_mode=False)
		self.assertEqual(m, [[[0], [1]], [[], []], [[2], [3]], [[], []]])

if __name__ == '__main__':
	unittest.main()