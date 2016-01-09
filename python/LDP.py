"""
Half of the duo that made me a graduate.
There are some lines of Rama's code in this.
See the comment on line 63? I'd rather not.

This is one hell of ugly, convoluted code.

The commit log from years ago:
Riyad Rivandi	d29a17c		final?				2015-01-12
Riyad Rivandi	3f81ecd		AIRS kelar?			2014-12-29
Riyad Rivandi	b948a09		mutate cell AIRS	2014-12-29
Riyad Rivandi	4f10d30		AIRS + Buku			2014-12-28
Riyad Rivandi	a6a32bc		avg. LDP			2014-12-25
Riyad Rivandi	ee669c4		hahaha				2014-12-23 
"""

from __future__ import division
import itertools

def group(data, n):
    l = len(data)
    return [data[i:i+n] for i in xrange(0, l, n)]
 
def ft(data):
    def generator():
        for line in data:
            for e in line:
                yield e
    return list(generator())

class LDP:
	def __init__(self, n, k):
		self.n = n
		self.k = k

	def histogramize(self, data):
		histograms = []
		for x in xrange(len(data)):
			region = list(itertools.chain(*data[x]))
			histogram = [0 for n in xrange(256)]
			for x in xrange(len(histogram)):
				histogram[region[x]] += 1
			mx = max(histogram)
			norm_histogram = map(lambda x:x/mx, histogram)
			histograms.append(norm_histogram)
		return histograms

	def flatten(self, arr3d):                
		arr4d = group(arr3d, self.n)        
		ordered = [zip(*e) for e in arr4d]        
		return ft(ft(ft(ordered)))

	def regionize(self, data, cWidth=21, cHeight=21, imWidth=126, imHeight=126):
		
		def croper(x, y, w, h):
			return [line[x:x+w] for line in arr2d[y:y+h]]            
			"""
			cWidth, cHeight, imWidth, imHeight, harus disesuaikan, tergantung ukuran gambar.
			"""        
		arr2d = group(data, imWidth)
		cropped = [croper(x, y, cWidth, cHeight) for y in xrange(0, imHeight, cHeight) for x in xrange(0, imWidth, cWidth)]
		return cropped

	def encode(self, regions):
			
		##revisit this ugly section someday
		def convolute(data, k):

			def countNeighborValue(neighbor, k):
				value = [0 for x in xrange(len(neighbor))]
				key = sorted(range(len(neighbor)), key=lambda x:neighbor[x], reverse=True)
				for x in xrange(k): value[key[x]] = 1
				return int(''.join(str(x) for x in value), 2)
			mask = [[] for i in xrange(8)]
			mask[0] = [[-3,-3,5],[-3,0,5],[-3,-3,5]]
			mask[1] = [[-3,5,5],[-3,0,5],[-3,-3,-3]]
			mask[2] = [[5,5,5],[-3,0,-3],[-3,-3,-3]]
			mask[3] = [[5,5,-3],[5,0,-3],[-3,-3,-3]]
			mask[4] = [[5,-3,-3],[5,0,-3],[5,-3,-3]]
			mask[5] = [[-3,-3,-3],[5,0,-3],[5,5,-3]]
			mask[6] = [[-3,-3,-3],[-3,0,-3],[5,5,5]]
			mask[7] = [[-3,-3,-3],[-3,0,5],[-3,5,5]]
			result = [[0 for x in xrange(len(data))] for y in xrange(len(data))]
			for a in xrange(len(data)):
				for b in xrange(len(data[0])):
					neighbor = [0 for z in xrange(8)]
					for x in xrange(-1,2):
						for y in xrange(-1,2):
							weight = 0
							position = 7
							position = 6 if (y == 1 and x == -1) else position
							position = 5 if (y == 0 and x == -1) else position
							position = 4 if (y == -1 and x == -1) else position
							position = 3 if (y == -1 and x == 0) else position
							position = 2 if (y == -1 and x == 1) else position
							position = 1 if (y == 0 and x == 1) else position
							position = 0 if (y == 1 and x == 1) else position
							if (a+x < len(data)) and (a+x >= 0) and (x!=0 or y!=0):
								if (b+y < len(data[0])) and (b+y >= 0):
									for m in xrange(-1,2):
										for n in xrange(-1,2):
											if (a+m < len(data)) and (a+m >= 0) and (m!=0 or n!=0):
												if (b+n < len(data[0])) and (b+n >= 0):
													weight = weight+data[a+m][b+n]*mask[position][m+1][n+1]
							neighbor[position] = weight
					result[a][b] = countNeighborValue(neighbor, k)
					# result[a][b] = 255 if countNeighborValue(neighbor, k) > 64 else 0
			return result
		## end of ugly section
		result = []
		k = self.k
		[result.append(convolute(regions[i], k)) for i in xrange(len(regions))]
		return result
