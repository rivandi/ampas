#!/usr/bin/env python

"""
Half-hearted implementation of 
https://en.wikipedia.org/wiki/Canopy_clustering_algorithm
"""

import mathlib
import random
from collections import defaultdict

def calculate_similarity(history):
	"""
	Function: calculate_similarity
	Summary: calculate cosine similarity between user
	Examples: 
	Attributes:
		@param (history):
			{
				'u1':[0,1,1,1,0],
				'u2':[0,1,1,1,0],
				'u3':[0,1,1,1,0]
			}
	Returns:
		{
			'u1': {'u2': 0.4, 'u3': 0.5},
			'u2': {'u1': 0.4, 'u3': 0.6},
			'u3': {'u1': 0.5, 'u3': 0.6},
		}
	"""	
	result = defaultdict(dict)
	users = list(history.iterkeys())
	for i, user1 in enumerate(users):
		for user2 in users[i+1:]:
			x = history[user1]
			y = history[user2]
			distance = mathlib.cosine(x, y)
			result[user1][user2] = distance
			result[user2][user1] = distance
	return result

def cluster_canopy(user_similarity, loose, tight):
	"""
	Function: cluster_canopy
	Summary: 
		cluster user based on similarity, canopy style
	Examples:
	Attributes: 
		@param (user_similarity):{
			'u1': {'u2': 0.4, 'u3': 0.5},
			'u2': {'u1': 0.4, 'u3': 0.6},
			'u3': {'u1': 0.5, 'u3': 0.6},
		}
		@param (loose): float, lower bound
		@param (tight): float, upper bound
	Returns: {
		0: [1, 2, 3, 6, 7, 8, 9],
		1: [2, 3, 5, 6, 8, 9],
		2: [8, 9, 4, 5],
		3: [8, 5, 6]
	}
	"""

	if loose > tight:
		tight, loose = loose, tight
	users = set(user_similarity.keys())
	clusters = defaultdict(set)
	cluster_number = 0

	while users:
		center = users.pop()
		cluster = set([center])
		removable = set()

		for candidate in users:
			score = user_similarity[center][candidate]
			if score > tight:
				cluster.add(candidate)
				removable.add(candidate)
			elif score > loose:
				cluster.add(candidate)

		for x in removable:
			users.remove(x)

		if cluster:
			clusters[cluster_number] = cluster
			cluster_number += 1
	return clusters

if __name__ == '__main__':
	history = {}
	for u in xrange(1,10):
		h = [random.randint(0, 1) for y in xrange(10)]
		history[u] = h
	user_similarity = calculate_similarity(history)
	loose = 0.4
	tight = 0.7
	s = count_canopy(user_similarity, loose, tight)