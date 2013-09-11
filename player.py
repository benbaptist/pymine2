import packets, struct, random, threading, time, traceback, zlib, string
class Prepare:
	def __init__(self, socket, addr, world, server):
		self.socket = socket
		self.addr = addr
		self.world = world
		self.server = server
		self.abort = False
		self.packetRecv = packets.PacketRecv(socket)
		self.packetSend = packets.PacketSend(socket)
	def wrap(self):
		try:
			self.listen()
		except:
			pass
	def listen(self):
		while True:
			packet = self.packetRecv.parse()
			if packet['id'] == 'invalid':
				print "invalid packet ID %s" % str(struct.pack('B', packet['packet']).encode('hex'))
				self.packetSend.kick('Invalid Packet %s' % str(struct.pack('B', packet['packet'])).encode('hex'))
				self.abort = True
				return False
			if packet['id'] == 0x02:
				self.username = packet['username']
				self.packetSend.login_request(entity_id=25, game_mode=1)
				self.packetSend.spawn_position()
				self.packetSend.map_chunk_bulk()
				self.packetSend.player_position_look(ystance=256, stancey=256)
				break
			if packet['id'] == 0xfa:
				#print packet['channel']
				if packet['channel'] == 'MC|PingHos':
				#print "its a poll!"
					self.packetSend.kick(u'\u0000'.join([u'\xa71', '74', '1.6.2', self.server.configData['motd'], str(len(self.server.get_players())), str(self.server.configData['max-players'])]))
					self.abort = True
					return False
		#id = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
		self.server.players[self.username] = Player(self.socket, self.addr, self.world, self.server, id)
		t = threading.Thread(target=self.server.players[self.username].wrap, args=())
		t.start()
		self.server.players[self.username].username = self.username
class Player:
	def __init__(self, socket, addr, world, server, id):
		self.socket = socket
		self.addr = addr
		self.world = world
		self.server = server
		self.abort = False
		self.id = id
		self.packetRecv = packets.PacketRecv(socket)
		self.packetSend = packets.PacketSend(socket)
	def keepalive(self):
		while not self.abort:
			self.packetSend.keepalive(random.randrange(0, 99999))
			time.sleep(1)
	def wrap(self):
		try:
			self.listen()
		except Exception,err:
			del self.server.players[self.username]
			print traceback.format_exc()
			self.packetSend.kick('Internal Server Error')
		try:
			self.username
		except:
			return False
		del self.server.players[self.username]
		self.abort = True
		self.server.part(self)
		time.sleep(1)
		self.socket.close()
	def listen(self):
		t = threading.Thread(target=self.keepalive, args=())
		t.start()
		self.packetSend.chat(u'\x00\xa7aType /terrain to see terrain! (for whatever reason, this fails to work on-connect as it crashes the game)')
		self.server.join(self)
		#for xC in range(16):
#			for zC in range(16):
#				data = ''
#				for x in range(16):
#					for y in range(512):
#						for z in range(16):
#							data += '\x02'
#				cData = zlib.compress(data)
#				self.packetSend.chunk_data(x=xC, z=zC, groundup=True, primary_bit_map=31, add_bit_map=0, data=cData)
		while not self.abort:
			try:
				packet = self.packetRecv.parse()
			except:
				self.abort = True
				break
			if packet['id'] == 'invalid':
				print "invalid packet ID %s" % str(struct.pack('B', packet['packet']).encode('hex'))
				self.packetSend.kick('Invalid Packet %s' % str(struct.pack('B', packet['packet'])).encode('hex'))
				self.abort = True
				break
			if packet['id'] == 0x03:
				#print "<%s> %s" % (self.username, packet['message'].encode('hex'))
				if packet['message'][0] == '/':
					# command
					def a(i):
						try: return packet['message'].split(' ')[i]
						except: return ""
					self.server.log.info("%s issued command: %s" % (self.username, packet['message']))
					if a(0)[1:] == 'randblocks':
						self.packetSend.chat('Filling world...')
						for xC in range(16):
							for zC in range(16):
								data = ''
								for x in range(16):
									for y in range(512):
										for z in range(16):
											data += struct.pack('B', random.randrange(0, 30))
								cData = zlib.compress(data)
								self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=31, add_bit_map=0, data=cData)
					if a(0)[1:] == 'blocks':
						self.packetSend.chat('Filling world...')
						for xC in range(16):
							for zC in range(16):
								data = ''
								for x in range(16):
									for y in range(256):
										for z in range(16):
											data += '\x02\x03\x03'
								cData = zlib.compress(data)
								self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=15, add_bit_map=0, data=cData)
					if a(0)[1:] == 'tower':
						self.packetSend.chat('Filling world...')
						for xC in range(16):
							for zC in range(16):
								data = ''
								for x in range(16):
									for y in range(250):
										for z in range(16):
											data += '\x02'
								for y in range(250):
									for x in range(16):
										for z in range(16):
											data += '\xff'
								for y in range(250):
									for x in range(16):
										for z in range(16):
											data += '\xff'
								for x in range(256):
									data += struct.pack('B', 21)
								cData = zlib.compress(data)
								self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=65535, add_bit_map=0, data=cData)
					if a(0)[1:] == 'layered':
						self.packetSend.chat('Filling world...')
						for xC in range(16):
							for zC in range(16):
								data = ''
								id = 1
								for y in range(250):
									if id > 10: id = 1
									for x in range(16):
										for z in range(16):
											data += struct.pack('B', id)
									id += 1
								for y in range(250):
									for x in range(16):
										for z in range(16):
											data += '\xff'
								for y in range(250):
									for x in range(16):
										for z in range(16):
											data += '\xff'
								cData = zlib.compress(data)
								self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=65535, add_bit_map=0, data=cData)
					if a(0)[1:] == 'terrain':
						self.packetSend.chat('Filling world...')
						for xC in range(16):
							for zC in range(16):
								data = ''
								for y in range(180):
									for x in range(16):
										for z in range(16):
											data += struct.pack('B', 1)
								for y in range(random.randrange(2, 10)):
									for x in range(16):
										for z in range(16):
											data += struct.pack('B', 3)
								for x in range(16):
									for z in range(16):
										data += struct.pack('B', 2)
								for y in range(200):
									for x in range(16):
										for z in range(16):
											data += '\xff'
								for y in range(200):
									for x in range(16):
										for z in range(16):
											data += '\xff'
								cData = zlib.compress(data)
								self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=65535, add_bit_map=0, data=cData)
					if a(0)[1:] == 'waterworld':
						self.packetSend.chat('Filling world...')
						for xC in range(16):
							for zC in range(16):
								data = ''
								for x in range(16):
									for y in range(512):
										for z in range(16):
											data += '\x0a'
								cData = zlib.compress(data)
								self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=31, add_bit_map=0, data=cData)
					if a(0)[1:] == 'wack':
						self.packetSend.chat(u'\xa7aType /blocks to see terrain! (for whatever reason, this fails to work on-connect as it crashes the game)')
						#self.packetSend.chat(u'\xa7aWOOOOOOOOO space . {}[]\-0()1u43ofnkas')
						#for x in range(16):
						#	for y in range(256):
						#		for z in range(16):
						#			data += '\x02'
						#for x in range(16):
						#	for y in range(256):
						#		for z in range(16):
						#			data += '\x02'
						#for x in range(256):
						#	data += '\xff'
						#			data += '\x00
									#self.packetSend.block_change(x=x, y=y, z=z, block_type=random.randrange(1,5), metadata=0)
									#print '%s:%s:%s' % (str(x), str(y), str(z))
						self.packetSend.chat('Done.')
				else:
					self.server.chat(self, packet['message'])
				#self.packetSend.chat("<%s> %s" % (self.username, packet['message'].strip('\x00')))
			if packet['id'] == 0xcc:
				pass