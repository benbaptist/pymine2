from chunk import Chunk
class Terrain:
	def __init__(self, seed):
		self.seed = seed
	def generate(self, x, z):
		chunk = Chunk()
		for y in range(64):
			for x in range(16):
				for z in range(16):
					chunk.block(x, y, z)[0] = '\xff'
		return chunk