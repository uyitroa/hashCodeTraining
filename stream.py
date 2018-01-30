class StreamLoli:
	
	def __init__(self, vid_desc, resq_desc, cache_desc, latency):

		self.vid_desc, self.amount_vid = vid_desc, len(vid_desc)
		self.latency, self.endpoints = latency, len(latency)
		self.resq_desc, self.amount_resq = resq_desc, len(resq_desc)
		self.amount_cache, self.cache_desc = cache_desc[0],cache_desc
	

	def bubbleSort(self, lst, condition = "lst[x] < lst[x + 1]"):
		# args: [1,2,3] or [(1,2),(3,0)], condition
		for passLeft in range(len(lst) - 1, 0, -1):
			for x in range(passLeft):
				if eval(condition):
					lst[x], lst[x + 1] = lst[x + 1], lst[x]
		return lst




#test, <3 loli
vid_desc =  [50,50,80,30,110]
latency = [[(1000),(0,100),(2,200),(1,300)],[(500)]]
resq_desc = [(3,0,1500),(0,1,1000),(4,0,500),(1,0,1000)]
cache_desc = (3,100)

stream = StreamLoli(vid_desc, resq_desc, cache_desc, latency)
    
