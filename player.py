import packets, struct, random, threading, time, traceback, zlib, string, builtin_commands, math
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
				try:
					packet = self.packetRecv.parse()
				except:
					self.server.log.error('%s lost connection' % self.addr[0])
					return False
				if packet['id'] == 'invalid':
					print "invalid packet ID %s" % str(struct.pack('B', packet['packet']).encode('hex'))
					self.packetSend.kick('Invalid Packet %s' % str(struct.pack('B', packet['packet'])).encode('hex'))
					self.abort = True
					return False
				if packet['id'] == 0x02:
					self.username = packet['username']
					if self.username in self.server.players:
						try:
							self.server.players[self.username].disconnect(reason='Logged in from another location')
						except:
							pass
					self.packetSend.login_request(entity_id=25, game_mode=1)
					self.packetSend.spawn_position(*self.world.spawnPoint)
					# Let's do some testing.. (Tests failed)
					self.packetSend.map_chunk_bulk()
					#chunk_bulk = open('packet0x38.bin', 'rb')
					#self.socket.send(chunk_bulk.read())
					self.packetSend.player_position_look(x=self.world.spawnPoint[0], ystance=self.world.spawnPoint[1], stancey=self.world.spawnPoint[1], z=self.world.spawnPoint[2])
					break
				if packet['id'] == 0xfa:
					# MC|PingHost is how the client's server list is populated with data. 
					if packet['channel'].startswith('MC|PingHos'):
						self.packetSend.kick(u'\u0000'.join([u'\xa71', '74', '1.6.2', self.server.config['server-name'], str(len(self.server.get_players())), str(self.server.config['max-players'])]))
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
		self.entityID = random.randrange(0, 999999)
		self.packetRecv = packets.PacketRecv(socket)
		self.packetSend = packets.PacketSend(socket)
		self.chunksSent = []
		self.playersSent = []
		self.player = {}
		self.x = self.world.spawnPoint[0]
		self.y = self.world.spawnPoint[1]
		self.z = self.world.spawnPoint[2]
		
		#Ping calculation and keepalive variables.
		self.ping = 0
		
		#Send the first keepalive.
		self.last_keepalive_time = time.time()
		self.last_sent_keepalive = random.randrange(0, 99999)
		self.packetSend.keepalive(self.last_sent_keepalive)
		
	def info(self):
		pass
	def disconnect(self, reason=''):
		self.abort = True
		if len(reason) > 0:
				self.packetSend.kick(reason)
		self.server.part(self)
		self.socket.close()
		try:
				del self.server.players[self.username]
		except:
				pass
	def wrap(self):
		try:
				self.listen()
		except Exception, err:
				error = traceback.format_exc()
				for line in error.split('\n'):
					self.server.log.error(line)
				self.disconnect('Internal Server Error')
		try:
				self.username
		except:
				return False
		self.disconnect()
	def getPlayersInRange(self, range=200):
		playersInRange = []
		for player in self.server.get_players():
			x, y, z = player.x, player.y, player.z
			if abs(x-self.x) < range and abs(z-self.z) < range:
				playersInRange.append(player)
		return playersInRange
	def getChunkPos(self):
		x = math.floor(self.x/16)
		z = math.floor(self.z/16)
		return (x, z)
	def sendChunks(self, currentChunk, lastChunk=None):
		for xC in range(16):
			for zC in range(16):
				#test if chunk is not within lastChunk's bounds (hasn't been sent before)
				absX = currentChunk[0]-8+xC
				absZ = currentChunk[1]-8+zC
				if lastChunk == None or absX > lastChunk[0]+7 or absX < lastChunk[0]-8 or absZ > lastChunk[1]+7 or absZ < lastChunk[1]-8:
					data = ''
					for y in range(180):
							for x in range(16):
								for z in range(16):
									data += struct.pack('B', 1)
					for y in range(4):
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
					self.packetSend.chunk_data(x=currentChunk[0]+(xC-8), z=currentChunk[1]+(zC-8), groundup=True, primary_bit_map=65535, add_bit_map=0, data=cData)
	def listen(self):
		# This is where a MOTD would go
		if len(self.server.config['motd']) > 1:
			self.packetSend.chat(self.server.config['motd'])
		for p in self.server.get_players():
				self.packetSend.player_list_item(p.username, True, 0)
		spawnChunk = self.getChunkPos()
		self.sendChunks(spawnChunk)
		self.packetSend.player_position_look(x=self.world.spawnPoint[0], ystance=self.world.spawnPoint[1], stancey=self.world.spawnPoint[1], z=self.world.spawnPoint[2])
		time.sleep(0.2)
		self.server.join(self)
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
				#print (self.server.world.level['time'] / 24000.0)
				#Keepalive gets sent once in __init__ and goes on when we receive another keepalive.
				#self.packetSend.time_update(random.randrange(25, 59), random.randrange(0, 12000))
				self.packetSend.time_update(self.server.world.level['time'], math.floor((self.server.world.level['time'] / 24000.0) % 1 * 24000))
				if packet['id'] == 0x00:
					if packet['keepalive'] == self.last_sent_keepalive:
						self.ping = time.time() - self.last_keepalive_time
						self.last_keepalive_time = time.time()
						self.last_sent_keepalive = random.randrange(0, 99999)
						self.packetSend.keepalive(self.last_sent_keepalive)
						for pl in self.server.get_players():
							pl.packetSend.player_list_item(self.username, True, self.ping)
					else:
						print "Got wrong keepalive " + str(packet['keepalive']) + " from " + self.username + " (expecting " + str(self.last_sent_keepalive) + ")"
						self.disconnect("Got wrong keepalive.")
				
				if packet['id'] == 0x03:
					#print "<%s> %s" % (self.username, packet['message'].encode('hex'))
					if packet['message'][0] == '/':
						# The message is a command
						
						self.server.log.info("%s issued command: %s" % (self.username, packet['message']))
						splitted = packet["message"].split()
						command = splitted[0].lstrip("/")
						arguments = splitted[1:]
						
						self.server.EventManager.Command_Event(self.server, self, command, arguments)
						
						# temporary debug commands to figure out how SMP chunk data works
						# using 0x31s instead of a 0x38 could be causing the slow fill on client side
						if command == "randblocks":
								self.packetSend.chat('&eFilling world...')
								for xC in range(16):
									for zC in range(16):
										data = ''
										for x in range(16):
												for y in range(512):
													for z in range(16):
														data += struct.pack('B', random.randrange(0, 30))
										self.packetSend.player_position_look(x=0, ystance=260, z=0, on_ground=False) #Keep player from getting stuck
										cData = zlib.compress(data)
										self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=31, add_bit_map=0, data=cData)
								self.packetSend.chat('&aDone filling world!')
						elif command == "blocks":
								self.packetSend.chat('&eFilling world...')
								self.packetSend.chat('&cYou will be held in position (to avoid getting stuck), please wait..')
								for xC in range(16):
									for zC in range(16):
										data = ''
										for x in range(16):
												for y in range(256):
													for z in range(16):
														data += '\x02\x03\x03'
										self.packetSend.player_position_look(x=0, ystance=260, z=0, on_ground=False) #Keep player from getting stuck
										cData = zlib.compress(data)
										self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=15, add_bit_map=0, data=cData)
								self.packetSend.chat('&aDone filling world!')
						elif command == 'tower':
								self.packetSend.chat('&eFilling world...')
								self.packetSend.chat('&cYou will be held in position (to avoid getting stuck), please wait..')
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
										self.packetSend.player_position_look(x=0, ystance=260, z=0, on_ground=False) #Keep player from getting stuck
										cData = zlib.compress(data)
										self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=65535, add_bit_map=0, data=cData)
								self.packetSend.chat('&aDone filling world!')
						elif command == 'layered':
								self.packetSend.chat('&eFilling world...')
								self.packetSend.chat('&cYou will be held in position (to avoid getting stuck), please wait..')
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
										self.packetSend.player_position_look(x=0, ystance=260, z=0, on_ground=False) #Keep player from getting stuck
										cData = zlib.compress(data)
										self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=65535, add_bit_map=0, data=cData)
								self.packetSend.chat('&aDone filling world!')
						elif command == 'terrain':
								self.packetSend.chat('&eFilling world...')
								self.packetSend.chat('&cYou will be held in position (to avoid getting stuck), please wait..')
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
										self.packetSend.player_position_look(x=0, ystance=260, z=0, on_ground=False) #Keep player from getting stuck
										cData = zlib.compress(data)
										self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=65535, add_bit_map=0, data=cData)
								self.packetSend.chat('&aDone filling world!')
						elif command == 'waterworld':
								self.packetSend.chat('&eFilling world...')
								self.packetSend.chat('&cYou will be held in position (to avoid getting stuck), please wait..')
								for xC in range(16):
									for zC in range(16):
										data = ''
										for x in range(16):
												for y in range(512):
													for z in range(16):
														data += '\x0a'
										self.packetSend.player_position_look(x=0, ystance=260, z=0, on_ground=False) #Keep player from getting stuck
										cData = zlib.compress(data)
										self.packetSend.chunk_data(x=xC - 8, z=zC - 8, groundup=True, primary_bit_map=31, add_bit_map=0, data=cData)
								self.packetSend.chat('&aDone filling world!')
						elif command == 'wack':
								self.packetSend.chat(u'&'+str(random.randrange(0,9))+'Type /blocks to see terrain! (for whatever reason, this fails to work on-connect as it crashes the game)')
								self.packetSend.chat('Done.')
						else: 
							# New command interface.
							# Putting this here prevents it from catching any of the commands still implemented here.
							builtin_commands.run_command(self, command, arguments)
					else:
						self.server.chat(self, packet['message'])
					#self.packetSend.chat("<%s> %s" % (self.username, packet['message'].strip('\x00')))
				if packet['id'] == 0x0d or packet['id'] == 0x0b:
					lastChunk = self.getChunkPos()
					self.x = packet['x']
					self.y = packet['y_stance'] if packet['id'] == 0x0d else packet['y']
					self.z = packet['z']
					self.server.EventManager.Player_Move_Event(self.server, self, self.x, self.y, self.z)
					currentChunk = self.getChunkPos()
					if lastChunk != currentChunk:
						self.sendChunks(currentChunk, lastChunk)
					for player in self.getPlayersInRange(): # locate and determine if player is good
						if player.username not in self.playersSent and player.username is not self.username:
							self.packetSend.spawn_named_entity(entity_id=player.entityID, player_name=player.username, x=player.x, y=player.y, z=player.z, current_item=278, metadata={0: {"type": 0, "value": 0}})
							self.playersSent.append(player.username)
					#for player in self.getPlayersInRange():
					#	if self.username in player.playersSent and player.username is not self.username:
					#		player.packetSend.entity_teleport(entity_id=self.entityID, x=self.x, y=self.y, z=self.z) 
				if packet['id'] == 0xcc:
					pass
