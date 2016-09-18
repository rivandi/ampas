#!/usr/bin/env python3

"""
Complete rewrite of LDP.py, kinda useful for image edge response extraction.
This version provides LDPv option, which account for the contrast information [1].

[1] Local Directional Pattern Variance (LDPv): A Robust Feature Descriptor for Facial Expression Recognition
"""

import mathlib

def histogramize(matrix, histogram_size):
	histogram = [0 for x in range(histogram_size)]
	for x in matrix:
		for y in x:
			if y < histogram_size:
				histogram[y] += 1
	return histogram

if __name__ == '__main__':
	pass