"""
Half of the duo that made me a graduate.
This was my first "Machine Learning" code.

Line 21 to end haven't been touched by anyone in a year.
See? There is no that if __main__ thingy, no comment at all.

This sucks, there's a bug somewhere I don't remember.
The suckier thing is, I ported the core from a Ruby version.
Yet I still created a bug.

Ask me to modify this and I say nay.

The commit log from years ago:
Riyad Rivandi	d29a17c		final?				2015-01-12
Riyad Rivandi	3f81ecd		AIRS kelar?			2014-12-29
Riyad Rivandi	b948a09		mutate cell AIRS	2014-12-29
Riyad Rivandi	4f10d30		AIRS + Buku			2014-12-28
Riyad Rivandi	a6a32bc		avg. LDP			2014-12-25
Riyad Rivandi	ee669c4		hahaha				2014-12-23 
"""

from __future__ import division
import sys
import json 
import random
import operator
import math
import code
from collections import Counter

from operator import itemgetter as ig
def flatten(iterable):
        for line in iterable:
                for e in line:
                        yield e

class AIRS:

	def __init__(self, clone_rate, mutation_rate, stim_threshold, resource, vote):
		self.clone_rate = clone_rate
		self.mutation_rate = mutation_rate
		self.stim_threshold = stim_threshold
		self.resource = resource
		self.memcell = []
		self.k = vote
		self.max_dist = math.sqrt(256)

	def save_memcells(self, memcell):
		code = str(self.clone_rate)+'_'+str(self.mutation_rate)+'_'+str(self.stim_threshold)+'_'+str(self.resource)
		path = 'E:\TA\source\histogram'
		filename = path+"\jaffe.json"
		# filename = "_memcell_"+'code'+".json"
		#print 'saving '+filename
		json.dump(memcell, open(filename, 'wb'))

	def load_memcell(self, data):
		#print data+" loaded."
		self.memcell = json.load(open(data))

	def generate_memory_cells(self, data):
		def isExist(memory_cell, new_cell):
			for existing_cell in memory_cell:
				if new_cell["class"] == existing_cell["class"]:
					return True
			return False
		
		memory_cell = []
		cell_size = len(data) - 1
		# #print data
		while len(memory_cell) < 7:
			random_cell = data[random.randint(0, cell_size)]
			# dsds = random.randint(0, cell_size)
			cell_existence = isExist(memory_cell, random_cell)
			if not cell_existence:
				random_cell['stimulation'] = random.random()
				memory_cell.append(random_cell)
		return memory_cell

	def distance(self, a, b):
		def __(a):
			return operator.sub(a[0], a[1])**2
		return math.sqrt(reduce(operator.add, map(__, zip(a, b))))/self.max_dist

	def stimulate(self, population, stimulator):
		result = []
		stimulation, i = 0, 0
		for cell in population:
			d = self.distance(cell['histogram'], stimulator['histogram'])
			s = 1 - d
			# #print cell, d
			cell['stimulation'] = s
			result.append(cell)
		return result

	def get_most_stimulated_cell(self, memory_cell, antigen):
		stimulation_data = self.stimulate(memory_cell, antigen)
		return max(stimulation_data, key=lambda x: x['stimulation'])

	def generate_arb_pool(self, stimulated_cell):
		pool = []
		# #print stimulated_cell
		pool.append(stimulated_cell)
		stimulation = stimulated_cell['stimulation']
		num_clones = int(round(stimulation * self.clone_rate * self.mutation_rate))
		# #print num_clones
		for x in xrange(num_clones):
			mutated_clone = self.mutate(stimulated_cell)
			pool.append(mutated_clone)
		return pool

	def refine_arb_pool(self, pool, stimulated_cell):
		def __(x, y):
			return x + y['stimulation'] if type(x) != type(y) else x['stimulation'] + y['stimulation']

		#print 'refining arb...'
		mean_stim = 0
		candidate = []
		while mean_stim < self.stim_threshold:
			stimulated_pool = self.stimulate(pool, stimulated_cell)
			candidate = self.finest_cell(pool)			
			try:
				# code.interact(local=locals())
				# #print reduce(__, stimulated_pool, 0)
				#print stimulated_pool
				# exit()
				mean_stim = reduce(__, stimulated_pool, 0)/len(stimulated_pool)
				#print len(pool), mean_stim, self.stim_threshold 
			except:
				# #print sys.exc_info()
				# code.interact(local=locals())
				exit()

			if mean_stim < self.stim_threshold:
				#print '#',
				stimulated_pool = self.competition_for_resources(self, stimulated_pool)
				for cell in stimulated_pool:
					new_cell = self.mutate(cell)
					stimulated_pool.append(new_cell)
		return stimulated_pool

	def competition_for_resources(self, pool):
		def count_resource(cell):
			return cell['stimulation'] * self.clone_rate
		resource_pool = sorted(map(count_resource, pool), key=lambda x:x['stimulation'])
		total_resource = sum(resource_pool, key=lambda x:x['stimulation'])
		while total_resource > self.resource:
			total_resource -= resource_pool[-1]
			del resource_pool[-1]
		return resource_pool

	def mutate(self, cell):
		r = 1.0 - cell['stimulation']
		# #print 'stim',r
		# #print cell['histogram']
		for key, value in enumerate(cell['histogram']):
			mn = max(0.0, value-(r/2.0))
			mx = min(value+(r/2.0), 1.0)
			cell['histogram'][key] = mn + (random.random()*(mx-mn))
		return cell

	def finest_cell(self, pool):
		return max(pool, key=lambda x: x['stimulation'])

	def add_candidate_to_memory(self, memory_cell, stimulated_cell, candidate):
		# #print 
		if candidate['stimulation'] > stimulated_cell['stimulation']:
			# #print 'added..'
			memory_cell.append(candidate)
		# else:
			# #print 'discarded..'
		# #print
		return memory_cell

	def train(self, data):
		training_set = json.load(open(data))
		mc = {}
		for idx in training_set:
			class_data = training_set[idx]
			memory_cell = self.generate_memory_cells(class_data)
			for antigen in class_data:
				# print '.',
				stimulated_cell = self.get_most_stimulated_cell(memory_cell, antigen)
				if stimulated_cell['class'] != antigen['class']:
					memory_cell.append(antigen)
				else:
					pool = self.generate_arb_pool(stimulated_cell)
					#print stimulated_cell
					refined_pool = self.refine_arb_pool(pool, stimulated_cell)
					candidate = self.finest_cell(refined_pool)
					memory_cell = self.add_candidate_to_memory(memory_cell, stimulated_cell, candidate)
			print '.',
			mc[idx] = memory_cell
		print
		self.save_memcells(mc)

	def classify(self, antigen):
		
		def kNN(data, k):
			i = [data[x]['class'] for x in xrange(k)]
			return Counter(i).most_common()

		def whassername(data):
			flat = list(flatten(data))
			nameset = set(map(ig(0), flat))
			grouped = [[e for e in flat if e[0] == s] for s in nameset]
			ls = map(len, grouped)
			return sorted(zip(ls, nameset), reverse=True)[0][1]

		antigen_class = []
		for key in antigen:
			# print str(key)
			p = {'histogram':antigen[str(key)]}
			# print key, part
			# print len(self.memcell)
			pool = self.stimulate(self.memcell[str(key)], p)
			pc = kNN(sorted(pool, key=lambda x: x['stimulation'], reverse=True), self.k)
			antigen_class.append(pc)
		return whassername(antigen_class)

	def test(self, data):
		testing_set = json.load(open(data))
		correct = 0
		for i in testing_set:
			best = self.classify(i['histogram'])
			print best, i['class']
			correct += 1 if best == i['class'] else 0
		return (correct, len(testing_set))