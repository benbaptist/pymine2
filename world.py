from terrain import Terrain
from chunk import Chunk
	#def block(self, x, y, z):
	#	x1 = 
class World:
	def __init__(self, server, path):
		self.server = server
		self.time = 0
		self.seed = 0
		self.chunks = []
		self.entities = []
		self.path = path
		self.terrain = Terrain(self.seed)
	def populate(self):
		print "Populating world with chunks..."
		#for x in range(16):
		#	row = []
		#	for z in range(16):
		#		row.append(self.terrain.generate(x, z))
		#	self.chunks.append(row)
		#print self.chunks[0][0].blocks[0][0][0]
	def loop(self):
		while not self.server.abort:
			time.sleep(20/1000.0)