class Chunk:
	def __init__(self):
		#self.data = '\x00\x00\x00\x00\x00' * 4096 # 16-bit block ID, skylight, regular light, metadata byte
		self.blocks = []
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