import json, struct
class Chunk:
	def __init__(self):
		#self.data = '\x00\x00\x00\x00\x00' * 4096 # 16-bit block ID, skylight, regular light, metadata byte
		self.blocks = []
		self.dirty = True
		for y in range(256):
			ly = []
			for x in range(16):
				lx = []
				for z in range(16):
					lx.append(bytearray(5))
				ly.append(lx)
			self.blocks.append(ly)
	def block(self, x, y, z):
		return self.blocks[y][x][z]

class JSONChunk:
	def __init__(self):
		self.blocks = {}
		for y in xrange(256):
			self.blocks[y] = {}
			for z in xrange(16):
				self.blocks[y][z] = {}
				for x in xrange(16):
					self.blocks[y][z][x] = 0
		self.dirty = False
	def save_to_json(self):
		return json.dumps(self.blocks)
	def load_from_json(self, jsonstr):	
		self.blocks = json.loads(jsonstr)
	def get_block(self, y, z, x):
		return self.blocks[y][z][x]
	def set_block(self, y, z, x, block):
		self.blocks[y][z][x] = block
	def generate_data(self):
		data=''
		for y in xrange(256):
			for z in range(16):
				for x in range(16):
					data += struct.pack('B', self.blocks[y][z][x])
		return data		