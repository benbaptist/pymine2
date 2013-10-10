import struct, json
class PacketSend:
	def __init__(self, socket):
		self.socket = socket
	def byte(self, a):
		self.socket.send(struct.pack('>b', a))
	def ubyte(self, a):
		#print "Packet: %s" % struct.pack('>B', a).encode('hex')
		self.socket.send(struct.pack('>B', a))
	def short(self, a):
		#print "SEND SHORT: %s" % str(a)
		self.socket.send(struct.pack('>h', a))
	def ushort(self, a):
		self.socket.send(struct.pack('>H', a))
	def int(self, a):
		self.socket.send(struct.pack('>i', a))
	def long(self, a):
		self.socket.send(struct.pack('>q', a))
	def float(self, a):
		self.socket.send(struct.pack('>f', a))
	def double(self, a):
		self.socket.send(struct.pack('>d', a))
	def string16(self, a):
		self.short(len(a))
		self.socket.send(a.encode('utf-16be'))
	def boolean(self, a):
		if a:
			self.byte(1)
		else:
			self.byte(0)
	def slot(self, a):
		pass
	def metadata(self, a):
		for key, entry in a.iteritems():
			byte = (key & 0x1F) | (entry["type"] << 5)
			self.ubyte(byte)
			if entry["type"] == 0:
				self.byte(entry["value"])
			elif entry["type"] == 1:
				self.short(entry["value"])
			elif entry["type"] == 2:
				self.int(entry["value"])
			elif entry["type"] == 3:
				self.float(entry["value"])
			elif entry["type"] == 4:
				self.string16(entry["value"])
			elif entry["type"] == 5:
				self.slot(entry["value"])
			elif entry["type"] == 6:
				self.int(entry["value"][0])
				self.int(entry["value"][1])
				self.int(entry["value"][2])
		self.ubyte(127)
	def keepalive(self, id):
		self.ubyte(0x00)
		self.int(id)
	def login_request(self, entity_id=0, level_type='', game_mode=0, dimension=0, difficulty=0, max_players=20):
		self.ubyte(0x01)
		self.int(entity_id)
		self.string16(level_type)
		self.byte(game_mode)
		self.byte(dimension)
		self.byte(difficulty)
		self.byte(0x00)
		self.byte(max_players)
	def chat(self, text=''):
		self.ubyte(0x03)
		self.string16(json.dumps({'text':text}))
	def time_update(self, age_of_world=0, time_of_day=0):
		self.ubyte(0x04)
		self.long(age_of_world)
		self.long(time_of_day)
	def spawn_position(self, x=0, y=0, z=0):
		self.ubyte(0x06)
		self.int(x)
		self.int(y)
		self.int(z)
	def player_position_look(self, x=0, ystance=0, stancey=0, z=0, yaw=0, pitch=0, on_ground=True):
		self.ubyte(0x0d)
		self.double(x)
		self.double(ystance)
		self.double(stancey)
		self.double(z)
		self.float(yaw)
		self.float(pitch)
		self.boolean(on_ground)
	def spawn_named_entity(self, entity_id=0, player_name='', x=0, y=0, z=0, yaw=0, pitch=0, current_item=0, metadata={}):
		self.ubyte(0x14)
		self.int(entity_id)
		self.string16(player_name)
		self.int(x)
		self.int(y)
		self.int(z)
		self.byte(yaw)
		self.byte(pitch)
		self.short(current_item)
		self.metadata(metadata)
	def entity_teleport(self, entity_id=0, x=0, y=0, z=0, yaw=0, pitch=0):
		self.ubyte(0x22)
		self.int(entity_id)
		self.int(x)
		self.int(y)
		self.int(z)
		self.byte(yaw)
		self.byte(pitch)
	def chunk_data(self, x=0, z=0, groundup=True, primary_bit_map=0, add_bit_map=0, data=''):
		self.ubyte(0x33)
		self.int(x)
		self.int(z)
		self.boolean(groundup)
		self.ushort(primary_bit_map)
		self.ushort(add_bit_map)
		self.int(len(data))
		self.socket.send(data)
	def block_change(self, x=0, y=0, z=0, block_type=0, metadata=0):
		self.ubyte(0x35)
		self.int(x)
		self.byte(y)
		self.int(z)
		self.short(block_type)
		self.byte(metadata)
	def map_chunk_bulk(self, chunk_col_count=0, sky_light=True, data='', meta=''):
		self.ubyte(0x38)
		self.short(chunk_col_count)
		self.int(len(data))
		self.boolean(sky_light)
		self.socket.send(data)
	def named_sound_effect(self, sound_name, effect_x, effect_y, effect_z, volume=100.0, pitch=1):
		self.ubyte(0x3e)
		self.string16(sound_name)
		self.int(effect_x)
		self.int(effect_y)
		self.int(effect_z)
		self.float(volume)
		self.byte(pitch)
	def player_list_item(self, player_name='', online=True, ping=0):
		self.ubyte(0xc9)
		self.string16(player_name)
		self.boolean(online)
		self.short(ping)
	def tab_complete(self, text_to_complete):
		self.ubyte(0xCB)
		self.string16(text_to_complete)
	def client_statuses(self, payload=0):
		self.ubyte(0xcd)
		self.byte(payload)
	def encryption_key_request(self, server_id='', public_key=b'', verify_token=b''):
		self.ubyte(0xfd)
		self.string16(server_id)
		self.byte(len(public_key))
		for i in public_key:
			self.byte(i)
		self.byte(len(verify_token))
		for i in verify_token:
			self.byte(i)
	def kick(self, message):
		self.ubyte(0xff)
		self.string16(message)
	def send(self, packet):
		print "sending %s" % str(packet[0])
		if packet[0] == 0x03:
			self.byte(3)
			self.string16(packet[1])
class PacketRecv:
	def __init__(self, socket):
		self.socket = socket
	def byte(self):
		return struct.unpack('>b', self.socket.recv(1))[0]
	def ubyte(self):
		return struct.unpack('>B', self.socket.recv(1))[0]
	def short(self):
		return struct.unpack('>h', self.socket.recv(2))[0]
	def int(self):
		return struct.unpack('>i', self.socket.recv(4))[0]
	def long(self):
		return struct.unpack('>q', self.socket.recv(8))[0]
	def float(self):
		return struct.unpack('>f', self.socket.recv(4))[0]
	def double(self):
		return struct.unpack('>d', self.socket.recv(8))[0]
	def string16(self):
		length = self.short() * 2
		string = self.socket.recv(length)
		#if len(string) < length:
		#	raise Exception('Buffer Underrun')
		return u'' + string.replace('\x00', '') # .decode('utf-16be')
	def boolean(self):
		if self.byte() == 0x00:
			return False
		else:
			return True
	def slot(self):
		id = self.short()
		print id
		if id == -1:
			print "Empty slot!"
		else:
			count = self.byte()
			damage = self.short()
			length = self.short()
			nbt = ''
			if length > 0:
				nbt = self.socket.recv(length)
			return {'id': id, 'count': count, 'damage': damage, 'nbt': nbt}
		return {'id': id, 'count': 0, 'damage': 0, 'nbt': ''}
	def metadata(self):
		metadata = {}
		while True:
			byte = self.ubyte()
			if byte == 127:
				break
			key = byte & 0x1F
			valueType = byte >> 5
			entry = {"type": valueType}
			if valueType == 0:
				entry["value"] = self.byte()
			elif valueType == 1:
				entry["value"] = self.short()
			elif valueType == 2:
				entry["value"] = self.int()
			elif valueType == 3:
				entry["value"] = self.float()
			elif valueType == 4:
				entry["value"] = self.string16()
			elif valueType == 5:
				entry["value"] = self.slot()
			elif valueType == 6:
				entry["value"] = (self.int(), self.int(), self.int())
			metadata[key] = entry
		return metadata
	def parse(self):
		packet = struct.unpack('B', self.socket.recv(1))[0]
		#print 'received: %s' % struct.pack('B', packet).encode('hex')
		if packet == 0x00:
			return {'id': packet, 
				'keepalive': self.int()
			}
		if packet == 0x01:
			return {'id': packet,
				'entity_id': self.int(),
				'level_type': self.string16(),
				'game_mode': self.byte(),
				'dimension': self.byte(),
				'difficulty': self.byte(),
				'not_used': self.byte(),
				'max_players': self.byte()
			}
		if packet == 0x02:
			return {'id': packet,
				'protocol_version': self.byte(),
				'username': self.string16(),
				'server_host': self.string16(),
				'server_port': self.int()
			}
		if packet == 0x03:
			return {'id': packet,
				'message': self.string16()
			}
		if packet == 0x04:
			return {'id': packet,
				'age_of_world': self.long(),
				'time_of_day': self.long()
			}
		if packet == 0x05:
			item = {}
			return {'id': packet,
				'entity_id': self.int(),
				'slot': self.short(),
				'item': item
			}
		if packet == 0x06:
			return {'id': packet,
				'x': self.int(),
				'y': self.int(),
				'z': self.int()
			}
		if packet == 0x07:
			return {'id': packet,
				'user': self.int(),
				'target': self.int(),
				'mouse_button': self.boolean()
			}
		if packet == 0x08:
			return {'id': packet,
				'health': self.float(),
				'food': self.short(),
				'food_saturation': self.float()
			}
		if packet == 0x09:
			return {'id': packet, 
				'dimension': self.int(),
				'difficulty': self.byte(),
				'game_mode': self.byte(),
				'world_height': self.short(),
				'level_type': self.string16()
			}
		if packet == 0x0a:
			return {'id': packet,
				'on_ground': self.boolean()
			}
		if packet == 0x0b:
			return {'id': packet,
				'x': self.double(),
				'y': self.double(),
				'stance': self.double(),
				'z': self.double(),
				'on_ground': self.boolean()
			}
		if packet == 0x0c:
			return {'id': packet,
				'yaw': self.float(),
				'pitch': self.float(),
				'on_ground': self.boolean()
			}
		if packet == 0x0d:
			return {'id': packet,
				'x': self.double(),
				'y_stance': self.double(),
				'stance_y': self.double(),
				'z': self.double(),
				'yaw': self.float(),
				'pitch': self.float(),
				'on_ground': self.boolean()
			}
		if packet == 0x0e:
			return {'id': packet,
				'status': self.byte(),
				'x': self.int(),
				'y': self.byte(),
				'z': self.int(),
				'face': self.byte()
		}
		if packet == 0x0f:
			return {'id': packet,
				'x': self.int(),
				'y': self.ubyte(),
				'z': self.int(),
				'direction': self.byte(),
				'held_item': self.slot(),
				'cursor_x': self.byte(),
				'cursor_y': self.byte(),
				'cursor_z': self.byte()
			}
		if packet == 0x10:
			return {'id': packet,
				'slot_id': self.short()
			}
		if packet == 0x11:
			return {'id': packet,
				'entity_id': self.int(),
				'unknown': self.byte(),
				'bed_x': self.int(),
				'bed_y': self.byte(),
				'bed_z': self.int()
			}
		if packet == 0x12:
			return {'id': packet,
				'entity_id': self.int(),
				'animation': self.byte()
			}
		if packet == 0x13:
			return {'id': packet,
				'entity_id': self.int(),
				'action_id': self.byte(),
				'jumpboost': self.int()
			}
		if packet == 0x65:
			return {'id': packet,
				'window_id': self.byte()
			}
		if packet == 0xca:
			return {'id': packet,
				'flags': self.byte(),
				'flying_speed': self.float(),
				'walking_speed': self.float()
			}
		if packet == 0xcb:
			return {'id': packet,
				'text': self.string16()
			}
		if packet == 0xcc:
			return {'id': packet,
				'locale:': self.string16(),
				'view_distance': self.byte(),
				'chat_flags': self.byte(),
				'difficulty': self.byte(),
				'show_cape': self.boolean()
			}
		if packet == 0xcd:
			return {'id': packet,
				'payload': self.byte()
			}
		if packet == 0x6b:
			return {'id': packet,
				'slot': self.short(),
				'item': self.slot()
			}
		if packet == 0xfa:
			channel = self.string16()
			length = self.short()
			data = self.socket.recv(length)
			#for i in range(length):
			#	data += str(self.byte())
			return {'id': packet,
				'channel': channel,
				'length': length,
				'data': data
			}
		if packet == 0xfe:
			return {'id': packet,
				'magic': self.byte()
			}
		if packet == 0xff:
			return {'id': packet,
				'reason': self.string16()
			}
		return {'id': 'invalid', 'packet': packet}
