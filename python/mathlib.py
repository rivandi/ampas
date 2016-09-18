#!/usr/bin/env python3

"""
collection of crappy, almost-useless math functions
"""

import math
from functools import reduce

def transpose(matrix):
	return zip(*matrix)

def divide(matrix, region=(1,1), zero_mode=True):
	"""Divide 2D array into several regions.
	
	The result will be numbered in left-right, top-down manner
		example:
			divide([
				[1, 2, 3],
				[4, 5, 6],
				[7, 8, 9],
				[10,11,12]
			], region=(2,3))
		divides vertical and horizontal axis into two and three parts respectively
		thus yields
			[[1,4], [2,5], [3,6], [7,10], [8,11], [9,12]].
		Result length for uneven split will be mapped to its ceiling
			ex:
				divide([,2,3,4,5], region=(1,3))
			zero_mode:
			 	[[1,2], [3,4], [5,0]]
			not zero_mode:
			 	[[1,2], [3,4], [5]]
	
	Arguments:
		matrix {2D array}
	
	Keyword Arguments:
		region {tuple} -- pair of vertical & horizontal area (default: {(1,1)})
		zero_mode {bool} -- make sure every little matrix has same number of element
			and replace missing ones with zero

	Returns:
		list of smaller matrices {2D array}
	"""
	result = []
	ver_area, hor_area = region
	src_height, src_width = len(matrix), len(matrix[0])
	res_height, res_width = -(-src_height // ver_area), -(-src_width // hor_area)

	for i, x in enumerate(range(ver_area)):
		for j, y in enumerate(range(hor_area)):

			# start, end index
			sv, ev = res_height*i, min(src_height, res_height*(i+1)) # vertical
			sh, eh = res_width*j, min(src_width, res_width*(j+1)) #horizontal

			if zero_mode:
				# zero matrix with size of res_height*res_width 
				mini = [[0 for y in range(res_width)] for x in range(res_height)]
				for k, m in enumerate(range(sv, ev)):
					for l, n in enumerate(range(sh, eh)):
						mini[k][l] = matrix[m][n]
			else:
				mini = [matrix[k][sh:eh] for k in range(sv, ev)]
			result.append(mini)
	return result

def dot_product(x, y):
	arr = map(lambda i: x[i] * y[i], range(0, min(len(x), len(y))))
	res = reduce(lambda a, b: a + b, arr)
	return res if res != 0 else 1

def euclidean_norm(l):
	m = math.sqrt(reduce(lambda x, y: x + (y ** 2), l))
	return m if m != 0 else 1

def cosine_similarity(x, y):
	return dot_product(x, y) / (euclidean_norm(x) * euclidean_norm(y))

def demlo_num(n):
	if type(n) is not int:
		return 0
	return sum(map(lambda x:10**x, range(n)))**2

def binet_fib(n):
	if type(n) is not int:
		return 0
	out = (math.sqrt(5)) * (2 ** n)
	plus = (1 + math.sqrt(5)) ** n
	minus = (1 - math.sqrt(5)) ** n
	diff = plus - minus
	return int(diff / out)

if __name__ == '__main__':
	pass