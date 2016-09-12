#!/usr/bin/env python3

"""
Half-hearted implementation of 
https://en.wikipedia.org/wiki/Canopy_clustering_algorithm
"""

from collections import defaultdict
from mathlib import cosine_similarity

def calculate_similarity(history):
	"""calculate cosine similarity between user
	
	[description]
	
	Arguments:
		history {dictionary of list of binary} --
			key <- user_id
			value <- list of user-item interaction (binary)
			example: 
			{
				'u1':[0,1,1,1,0],
				'u2':[0,1,1,1,0],
				'u3':[0,1,1,1,0]
			}
	Returns:
		dictionary of similarities --
			key <- user_id_1
			value <- dictionary of float
				key <- user_id_2
				value <- cosine similarity between history of user_id_1 and user_id_2
			example: 
			{
				'u1': {'u2': 0.4, 'u3': 0.5},
				'u2': {'u1': 0.4, 'u3': 0.6},
				'u3': {'u1': 0.5, 'u3': 0.6},
			}
	"""

	result = defaultdict(dict)
	users = list(history.keys())
	for i, user1 in enumerate(users):
		for user2 in users[i+1:]:
			x = history[user1]
			y = history[user2]
			distance = cosine_similarity(x, y)
			result[user1][user2] = distance
			result[user2][user1] = distance
	return result

def cluster_canopy(user_similarity, loose=0.3, tight=0.6):
	"""cluster user based on similarity, canopy style
	
	Arguments:
		user_similarity {dictionary of similarities} -- output of calculate_similarity
	
	Keyword Arguments:
		loose {number} -- lower bound for outer cluster (default: {0.3})
		tight {number} -- lower bound for inner cluster (default: {0.6})
	
	Returns:
		dictionary of list of user_id --
			key <- cluster id
			value <- list of cluster member
			{
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
	import random
	history = {}
	user_number = 10
	item_number = 10
	loose = 0.4
	tight = 0.7

	for u in range(user_number):
		h = [random.randint(0, 1) for y in range(item_number)]
		history[u] = h
	user_similarity = calculate_similarity(history)
	s = cluster_canopy(user_similarity, loose, tight)
	print(s)