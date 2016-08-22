#!/usr/bin/env python

"""
collection of crappy, almost-useless math functions
"""

from __future__ import division
import math
import datetime

def transpose(matrix):
	return zip(*matrix)

def dot(x, y):
	arr = map(lambda i: x[i] * y[i], range(0, min(len(x), len(y))))
	res = reduce(lambda a, b: a + b, arr)
	return res if res != 0 else 1

def magnitude(l):
	m = math.sqrt(reduce(lambda x, y: x + (y ** 2), l))
	return m if m != 0 else 1

def cosine(x, y):
	return dot(x, y) / (magnitude(x) * magnitude(y))

def demlo(n):
	return sum(map(lambda x:10**x, range(n)))**2

def binet(n):
	out = (math.sqrt(5)) * (2 ** n)
	plus = (1 + math.sqrt(5)) ** n
	minus = (1 - math.sqrt(5)) ** n
	diff = plus - minus
	return int(diff / out)

if __name__ == '__main__':
	pass