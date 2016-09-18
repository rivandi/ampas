import context
import mathlib
import unittest

class TestMathlib(unittest.TestCase):

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

if __name__ == '__main__':
	unittest.main()