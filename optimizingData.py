import numpy as np

class Fill:
	def __init__(self,row,column,unvai,pools,m_server,info_un,info_server):
		self.column = column
		self.row = row
		self.unvai = unvai
		self.pools = pools
		self.m_server = m_server
		self.info_un = info_un
		self.info_server = info_server

	def available_Slot(self):
		self.my_slots = np.ones((self.column,self.row),dtype = np.uint8)
		for x in range(self.unvai): # integrate unvailable slot
			coord = info_un[x]
			self.my_slots[coord[0],coord[1]] = 0

		my_line = []
		x_s = 0
		y_s = 0

		for l in range(self.row):
			for c in range(self.column):
				if self.my_slots[l,c] == 0:
					my_coord = (y_s,x_s,l,c-1) # problem: 0,0,... idfk
					my_line.append(my_coord)

r,s,u,p,m, = 3,5,2,3,7
unvai = [(0,0),(2,2)]
info_server = [(5,10),(5,9),(4,6),(2,4),(1,5),(1,2)]
