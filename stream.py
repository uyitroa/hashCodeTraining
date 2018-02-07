class StreamLoli:

	def __init__(self, vid_desc, resq_desc, cache_desc, latency):
		# variables: vid_desc, amount_vid, latency, end_points
		# resq_desc, amount_resq, amount_cache, cache_desc


		self.vid_desc, self.amount_vid = vid_desc, len(vid_desc)
		self.latency, self.endpoints = latency, len(latency)
		self.resq_desc, self.amount_resq = resq_desc, len(resq_desc)
		self.amount_cache, self.cache_desc = cache_desc[0], [cache_desc[1]] * cache_desc[0]
		self.solution = ["x"] * self.amount_cache


	def deal(self): # main function

		#rearrange resquest list to get most point
		condition = "lst[x][2] * self.vid_desc[lst[x][0]] < lst[x + 1][2] * self.vid_desc[lst[x + 1][0]]"
		self.resq_desc = self.bubbleSort(self.resq_desc,condition)

		#rearrange latency list by smallest to biggest
		for pos in range(len(self.latency)):
			my_distance = self.latency[pos]
			self.latency[pos] = self.bubbleSort(my_distance,"lst[x][1] > lst[x + 1][1]")

		#deal with resquest now
		for x in range(self.amount_resq):
			point = self.resq_desc[x][1]
			size = self.vid_desc[self.resq_desc[x][0]]
			my_index = self.set_cache(point,size) #suitable cache
			if my_index != -1:
				if self.solution[my_index] == "x":
					self.solution[my_index] = str(my_index) + " " + str(self.resq_desc[x][0])
				else:
					self.solution[my_index] += " " + str(self.resq_desc[x][0])
		print self.solution

	def bubbleSort(self, lst, condition = "lst[x] < lst[x + 1]"): #sort
		# args: [1,2,3] or [(1,2),(3,0)], condition

		for passLeft in range(len(lst) - 1, 0, -1):
			for x in range(passLeft):
				if eval(condition):
					lst[x], lst[x + 1] = lst[x + 1], lst[x]
		return lst

	def set_cache(self,point, size): # find the suitable cache for the request
		# args: endpoint: 0 or 1 or idk; size: 50mb, 30mb
		# return index of suitable cache, ex: 1 or 2 or 3
		
		connected_cache = self.latency[point]
		for x in range(len(connected_cache)):
			if connected_cache[x][0] == -1: # if direct
				return -1
			else:
				my_cache = self.cache_desc[connected_cache[x][0]] # cache_desc = [100,100,100] or [200,200,200]
				if size <= my_cache:
					self.cache_desc[connected_cache[x][0]] -= size
					if self.cache_desc[connected_cache[x][0]] < min(self.vid_desc): # optimize program to save time
						my_cache -= size
						self.cache_desc.remove(my_cache)
						self.amount_cache = len(self.cache_desc) # update amount_cache
					return connected_cache[x][0] # dis is index of cache




#test, <3 loli
vid_desc = [50, 50, 80, 30, 110]
latency = [[(-1, 1000), (0, 100), (2, 200), (1, 300)], [(-1, 500)]]
resq_desc = [(3, 0, 1500), (0, 1, 1000), (4, 0, 500), (1, 0, 1000)]
cache_desc = (3, 100)

stream = StreamLoli(vid_desc, resq_desc, cache_desc, latency)
stream.deal()
