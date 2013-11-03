import time, os, random, json, nbt
from terrain import Terrain
from chunk import Chunk, JSONChunk
	#def block(self, x, y, z):
	#	x1 = 
class World:
	def __init__(self, server, path):
		self.server = server
		self.chunks = {}
		self.entities = []
		self.spawnPoint = (8, 150, 8) #todo: use data from level.dat
		self.path = path
	def get_inmemory_chunk(self, x, z):
		self.chunks[x+z*8] = JSONChunk()
		return self.chunks[x+z*8]
	def populate(self):
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		if os.path.exists('%s/level.dat' % self.path):
			cantLoad = False
			f = open('%s/level.dat' % self.path, 'r')
			try:
				json.loads(f.read())
			except:
				cantLoad = True
				self.server.log.error('level.dat unreadable or unparsable - resetting')
			f.close()
		defaults = {'seed': random.randrange(-9999999, 9999999),
			'time': 0,
			'name': ''
		}
		if not os.path.exists('%s/level.dat' % self.path) or cantLoad:
			f = open('%s/level.dat' % self.path, 'w')
			f.write(json.dumps(defaults))
			f.close()
		f = open('%s/level.dat' % self.path, 'r')
		self.level = json.loads(f.read())
		f.close()
		self.terrain = Terrain(self.level['seed'])
		#for x in range(16):
		#	row = []
		#	for z in range(16):
		#		row.append(self.terrain.generate(x, z))
		#	self.chunks.append(row)
		#print self.chunks[0][0].blocks[0][0][0]
	def touch(self, x, z): # same as unix touch command, basically creates a chunk file if it doesn't exist, otherwise keeps it
		try:
			self.chunks[x][z]
		except:
			if os.path.exists('%s/chunks/%s,%s' % (self.path, str(x), str(z))):
				self.parseChunk(x, z)
			else:
				if x in self.chunks:
					self.chunks[x] = {}
				self.chunks[x][z] = self.terrain.generate(x, z)
		return self.chunks[x][z]
	def flush(self):
		f = open('%s/level.dat' % self.path, 'w')
		f.write(json.dumps(self.level))
		f.close()
	def loop(self):
		self.server.log.info('World tick loop begin')
		while not self.server.abort:
			self.level['time'] += 1
			time.sleep(.05) # 20 ticks/second is 1/20 (.05) seconds per tick
