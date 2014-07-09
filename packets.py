import struct, json, threading, varint
class PacketSend:
	def __init__(self, socket):
		self.socket = socket
		self.lock = threading.Lock()
	def byte(self, a):
		self.socket.send(struct.pack('>b', a))
	def ubyte(self, a):
		self.socket.send(struct.pack('>B', a))
	def short(self, a):
		self.socket.send(struct.pack('>h', a))
	def ushort(self, a):
		self.socket.send(struct.pack('>H', a))
	def int(self, a):
		self.socket.send(struct.pack('>i', a))
	def varint(self, a):
		self.socket.send(varint.pack_varint(a))
	def long(self, a):
		self.socket.send(struct.pack('>q', a))
	def float(self, a):
		self.socket.send(struct.pack('>f', a))
	def double(self, a):
		self.socket.send(struct.pack('>d', a))
	def string(self, a):
		self.varint(len(a))
		self.socket.send(a.encode('utf-8'))
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
		with self.lock:
			self.ubyte(0x00)
			self.int(id)
	def login_request(self, entity_id=0, level_type='', game_mode=0, dimension=0, difficulty=0, max_players=20):
		with self.lock:
			self.ubyte(0x01)
			self.int(entity_id)
			self.ubyte(game_mode)
			self.byte(dimension)
			self.ubyte(difficulty)
			self.ubyte(max_players)
			self.string(level_type)
	def chat(self, text=''):
		with self.lock:
			self.ubyte(0x02)
			self.string(json.dumps({'text':text}))
	def time_update(self, age_of_world=0, time_of_day=0):
		with self.lock:
			self.ubyte(0x03)
			self.long(age_of_world)
			self.long(time_of_day)
	def entity_equipment(self, entity_id=0, slot=0, item={}):
		with self.lock:
			self.ubyte(0x04)
			self.int(entity_id)
			self.short(slot)
			self.slot(item)
	def spawn_position(self, x=0, y=0, z=0):
		with self.lock:
			self.ubyte(0x05)
			self.int(x)
			self.int(y)
			self.int(z)
	def update_health(self, health=0, food=0, food_saturation=0):
		with self.lock:
			self.ubyte(0x06)
			self.float(health)
			self.short(food)
			self.float(food_saturation)
	def respawn(self, dimension=0, difficulty=0, gamemode=0, level_type=''):
		with self.lock:
			self.ubyte(0x07)
			self.int(dimension)
			self.ubyte(difficulty)
			self.ubyte(gamemode)
			self.string(level_type)
	def player_position_look(self, x=0, y=0, z=0, yaw=0, pitch=0, on_ground=True):
		with self.lock:
			self.ubyte(0x08)
			self.double(x)
			self.double(y)
			self.double(z)
			self.float(yaw)
			self.float(pitch)
			self.boolean(on_ground)
	def held_item_change(self, slot=0):
		with self.lock:
			self.ubyte(0x09)
			self.byte(slot)
	def use_bed(self, entity_id=0, x=0, y=0, z=0):
		with self.lock:
			self.ubyte(0x0A)
			self.int(entity_id)
			self.int(x)
			self.ubyte(y)
			self.int(z)
	def animation(self, entity_id=0, animation=0):
		with self.lock:
			self.ubyte(0x0B)
			self.varint(entity_id)
			self.ubyte(animation)
	def spawn_player(self, entity_id=0, player_uuid='', player_name='', data_count=0, data={}, x=0, y=0, z=0, yaw=0, pitch=0, current_item=0, metadata={}):
		with self.lock:
			self.ubyte(0x0C)
			self.varint(entity_id)
			self.string(player_uuid)
			self.string(player_name)
			self.varint(data_count)
			# Send data array
			self.int(x)
			self.int(y)
			self.int(z)
			self.byte(yaw)
			self.byte(pitch)
			self.short(current_item)
			self.metadata(metadata)
	def collect_item(self, collected_entity_id=0, collector_entity_id=0):
		with self.lock:
			self.ubyte(0x0D)
			self.int(collected_entity_id)
			self.int(collector_entity_id)
	def spawn_object(self, entity_id=0, type=0, x=0, y=0, z=0, pitch=0, yaw=0, data=0):
		with self.lock:
			self.ubyte(0x0E)
			self.varint(entity_id)
			self.byte(type)
			self.int(x)
			self.int(y)
			self.int(z)
			self.byte(pitch)
			self.byte(yaw)
			#Make this properly send object data
			self.int(data)
	def spawn_mob(self, entity_id=0, type=0, x=0, y=0, z=0, yaw=0, pitch=0, head_pitch=0, velocity_x=0, velocity_y=0, velocity_z=0, metadata={}):
		with self.lock:
			self.ubyte(0x0F)
			self.varint(entity_id)
			self.ubyte(type)
			self.int(x)
			self.int(y)
			self.int(z)
			self.byte(yaw)
			self.byte(pitch)
			self.byte(head_pitch)
			self.short(velocity_x)
			self.short(velocity_y)
			self.short(velocity_z)
			self.metadata(metadata)
	def spawn_painting(self, entity_id=0, title='', x=0, y=0, z=0, direction=0):
		with self.lock:
			self.ubyte(0x10)
			self.varint(entity_id)
			self.string(title)
			self.int(x)
			self.int(y)
			self.int(z)
			self.int(direction)
	def spawn_experience_orb(self, entity_id=0, x=0, y=0, z=0, count=0):
		with self.lock:
			self.ubyte(0x11)
			self.varint(entity_id)
			self.int(x)
			self.int(y)
			self.int(z)
			self.short(count)
	def entity_velocity(self, entity_id=0, velocity_x=0, velocity_y=0, velocity_z=0):
		with self.lock:
			self.ubyte(0x12)
			self.int(entity_id)
			self.short(velocity_x)
			self.short(velocity_y)
			self.short(velocity_z)
	def destroy_entities(self, entity_ids={}):
		with self.lock:
			self.ubyte(0x13)
			self.byte(len(entity_ids))
			for entity_id in entity_ids:
				self.int(entity_id)
	def entity(self, entity_id=0):
		with self.lock:
			self.ubyte(0x14)
			self.int(entity_id)
	def entity_relative_move(self, entity_id=0, change_x=0, change_y=0, change_z=0):
		with self.lock:
			self.ubyte(0x15)
			self.int(entity_id)
			self.byte(change_x)
			self.byte(change_y)
			self.byte(change_z)
	def entity_look(self, entity_id=0, yaw=0, pitch=0):
		with self.lock:
			self.ubyte(0x16)
			self.int(entity_id)
			self.byte(yaw)
			self.byte(pitch)
	def entity_look_relative_move(self, entity_id=0, change_x=0, change_y=0, change_z=0, yaw=0, pitch=0):
		with self.lock:
			self.ubyte(0x17)
			self.int(entity_id)
			self.byte(change_x)
			self.byte(change_y)
			self.byte(change_z)
			self.byte(yaw)
			self.byte(pitch)
	def entity_teleport(self, entity_id=0, x=0, y=0, z=0, yaw=0, pitch=0):
		with self.lock:
			self.ubyte(0x18)
			self.int(entity_id)
			self.int(x)
			self.int(y)
			self.int(z)
			self.byte(yaw)
			self.byte(pitch)
	def entity_head_look(self, entity_id=0, head_yaw=0):
		with self.lock:
			self.ubyte(0x19)
			self.int(entity_id)
			self.byte(head_yaw)
	def entity_status(self, entity_id=0, entity_status=0):
		with self.lock:
			self.ubyte(0x1A)
			self.int(entity_id)
			self.byte(entity_status)
	def attach_entity(self, entity_id=0, vehicle_id=0, leash=False):
		with self.lock:
			self.ubyte(0x1B)
			self.int(entity_id)
			self.int(vehicle_id)
			self.boolean(leash)
	def entity_metadata(self, entity_id=0, metadata={}):
		with self.lock:
			self.ubyte(0x1C)
			self.int(entity_id)
			self.metadata(metadata)
	def entity_effect(self, entity_id=0, effect_id=0, amplifier=0, duration=0):
		with self.lock:
			self.ubyte(0x1D)
			self.int(entity_id)
			self.byte(effect_id)
			self.byte(amplifier)
			self.short(duration)
	def remove_entity_effect(self, entity_id=0, effect_id=0):
		with self.lock:
			self.ubyte(0x1E)
			self.int(entity_id)
			self.byte(effect_id)
	def set_experience(self, experience_bar=0, level=0, total_experience=0):
		with self.lock:
			self.ubyte(0x1F)
			self.float(experience_bar)
			self.short(level)
			self.short(total_experience)
	def entity_properties(self, entity_id=0, properties={}):
		with self.lock:
			self.ubyte(0x20)
			self.int(entity_id)
			self.int(len(properties))
			#TODO: Send property data array
	def chunk_data(self, x=0, z=0, groundup=True, primary_bit_map=0, add_bit_map=0, data=''):
		with self.lock:
			self.ubyte(0x21)
			self.int(x)
			self.int(z)
			self.boolean(groundup)
			self.ushort(primary_bit_map)
			self.ushort(add_bit_map)
			self.int(len(data))
			self.socket.send(data)
	def multi_block_change(self, chunk_x=0, chunk_z=0, records={}):
		with self.lock:
			self.ubyte(0x22)
			self.int(chunk_x)
			self.int(chunk_z)
			self.short(len(records)/4)
			self.int(len(records))
			#Wiki says data size should always be 4 times count.
			#TODO: Send array of records
	def block_change(self, x=0, y=0, z=0, block_id=0, metadata=0):
		with self.lock:
			self.ubyte(0x23)
			self.int(x)
			self.ubyte(y)
			self.int(z)
			self.varint(block_id)
			self.ubyte(metadata)
	def block_action(self, x=0, y=0, z=0, byte1=0, byte2=0, block_type=0):
		with self.lock:
			self.ubyte(0x24)
			self.int(x)
			self.short(y)
			self.int(z)
			self.ubyte(byte1)
			self.ubyte(byte2)
			self.varint(block_type)
	def block_break_animation(self, entity_id=0, x=0, y=0, z=0, stage=0):
		with self.lock:
			self.ubyte(0x25)
			self.varint(entity_id)
			self.int(x)
			self.int(y)
			self.int(z)
			self.byte(stage)
	def map_chunk_bulk(self, chunk_col_count=0, sky_light=True, data='', meta=''):
		with self.lock:
			self.ubyte(0x26)
			self.short(chunk_col_count)
			self.int(len(data))
			self.boolean(sky_light)
			self.socket.send(data)
			#TODO: Send meta information
	def explosion(self, x=0, y=0, z=0, radius=0, records={}, motion_x=0, motion_y=0, motion_z=0):
		with self.lock:
			self.ubyte(0x27)
			self.float(x)
			self.float(y)
			self.float(z)
			self.float(radius)
			self.int(len(records)/3)
			for record in records:
				self.byte(record)
			self.float(motion_x)
			self.float(motion_y)
			self.float(motion_z)
	def effect(self, effect_id=0, x=0, y=0, z=0, data=0, disable_relative_volume=False):
		with self.lock:
			self.ubyte(0x28)
			self.int(effect_id)
			self.int(x)
			self.byte(y)
			self.int(z)
			self.int(data)
			self.boolean(disable_relative_volume)
	def sound_effect(self, name='', effect_x=0, effect_y=0, effect_z=0, volume=100.0, pitch=1):
		with self.lock:
			self.ubyte(0x29)
			self.string(name)
			self.int(effect_x)
			self.int(effect_y)
			self.int(effect_z)
			self.float(volume)
			self.ubyte(pitch)
	def particle(self, name='', x=0, y=0, z=0, offset_x=0, offset_y=0, offset_z=0, data=0, amount=0):
		with self.lock:
			self.ubyte(0x2A)
			self.string(name)
			self.float(x)
			self.float(y)
			self.float(z)
			self.float(offset_x)
			self.float(offset_y)
			self.float(offset_z)
			self.float(data)
			self.int(amount)
	def change_game_state(self, reason=0, value=0):
		with self.lock:
			self.ubyte(0x2B)
			self.ubyte(reason)
			if reason == 3 or reason == 5 or reason == 7:
				self.float(value)
	def spawn_global_entity(self, entity_id=0, bolt_type=1, x=0, y=0, z=0):
		with self.lock:
			self.ubyte(0x2C)
			self.varint(entity_id)
			self.byte(bolt_type)
			self.int(x)
			self.int(y)
			self.int(z)
	def open_window(self, window_id=0, inventory_type=0, window_title='', slot_amount=0, use_window_title=False, entity_id=0):
		with self.lock:
			self.ubyte(0x2D)
			self.ubyte(window_id)
			self.ubyte(inventory_type)
			self.string(window_title)
			self.ubyte(slot_amount)
			self.boolean(use_window_title)
			if inventory_type == 11:
				self.int(entity_id)
	def close_window(self, window_id=0):
		with self.lock:
			self.ubyte(0x2E)
			self.ubyte(window_id)
	def set_slot(self, window_id=0, slot=0, data={}):
		with self.lock:
			self.ubyte(0x2F)
			self.byte(window_id)
			self.short(slot)
			self.slot(data)
	def window_items(self, window_id=0, data={}):
		with self.lock:
			self.ubyte(0x30)
			self.ubyte(window_id)
			self.short(len(data))
			for slotdata in data:
				self.slot(slotdata)
	def window_property(self, window_id=0, window_property=0, value=0):
		with self.lock:
			self.ubyte(0x31)
			self.ubyte(window_id)
			self.short(window_property)
			self.short(value)
	def confirm_transaction(self, window_id=0, action_number=0, accepted=True):
		with self.lock:
			self.ubyte(0x32)
			self.short(action_number)
			self.boolean(accepted)
	def update_sign(self, x=0, y=0, z=0, line1='', line2='', line3='', line4=''):
		with self.lock:
			self.ubyte(0x33)
			self.int(x)
			self.short(y)
			self.int(z)
			self.string(line1)
			self.string(line2)
			self.string(line3)
			self.string(line4)
	def maps(self, item_damage=0, data={}):
		with self.lock:
			self.ubyte(0x34)
			self.varint(item_damage)
			self.short(len(data))
			self.socket.send(data)
	def update_block_entity(self, x=0, y=0, z=0, action=0, nbt_data={}):
		with self.lock:
			self.ubyte(0x35)
			self.int(x)
			self.short(y)
			self.int(z)
			self.ubyte(action)
			self.short(len(nbt_data))
			self.socket.send(nbt_data)
	def sign_editor_open(self, x=0, y=0, z=0):
		with self.lock:
			self.ubyte(0x36)
			self.int(x)
			self.int(y)
			self.int(z)
	def statistics(self, entries={}):
		with self.lock:
			self.ubyte(0x37)
			self.varint(len(entries))
			for stat_name, value in entries.iteritems():
				self.string(stat_name)
				self.varint(value)
	def player_list_item(self, player_name='', online=True, ping=0):
		with self.lock:
			self.ubyte(0x38)
			self.string(player_name)
			self.boolean(online)
			self.short(ping)
	def player_abilities(self, flags=0, fly_speed=0, walk_speed=0):
		with self.lock:
			self.ubyte(0x39)
			self.byte(flags)
			self.float(fly_speed)
			self.float(walk_speed)
	def tab_complete(self, count=0, matches={}):
		with self.lock:
			self.ubyte(0x3A)
			self.varint(count)
			for match in matches:
				self.string(match)
	def scoreboard_objective(self, name=0, value=0, action=0):
		with self.lock:
			self.ubyte(0x3B)
			self.string(name)
			self.string(value)
			self.byte(action)
	def update_score(self, item_name='', action=0, score_name='', value=0):
		with self.lock:
			self.ubyte(0x3C)
			self.string(item_name)
			self.byte(action)
			if not action == 1:
				self.string(score_name)
				self.int(value)
	def display_scoreboard(self, position=0, score_name=''):
		with self.lock:
			self.ubyte(0x3D)
			self.byte(position)
			self.string(score_name)
	def teams(self, team_name='', mode=0, display_name='', prefix='', suffix='', friendly_fire=0, players={}):
		with self.lock:
			self.ubyte(0x3E)
			self.byte(mode)
			if mode == 0 or mode == 2:
				self.string(display_name)
				self.string(prefix)
				self.string(suffix)
				self.byte(friendly_fire)
				self.short(len(players))
				for player in players:
					self.string(player)
	def plugin_message(self, channel='', data={}):
		with self.lock:
			self.ubyte(0x3F)
			self.string(channel)
			self.short(len(data))
			self.socket.send(data)
	def disconnect(self, reason):
		with self.lock:
			self.ubyte(0x40)
			self.string(reason)
	def client_statuses(self, payload=0):
		with self.lock:
			self.ubyte(0xcd)
			self.byte(payload)
	def encryption_key_request(self, server_id='', public_key=b'', verify_token=b''):
		with self.lock:
			self.ubyte(0xfd)
			self.string16(server_id)
			self.byte(len(public_key))
			for i in public_key:
				self.byte(i)
				self.byte(len(verify_token))
				for i in verify_token:
					self.byte(i)
	def kick(self, message):
		self.disconnect(message)
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
