import socket, threading, os, json, random, string
from player import Player
from player import Prepare
from world import World
from chat import Chat

class Server:
	def __init__(self, log):
		self.socket = socket.socket()
		self.abort = False
		self.players = {}
		self.log = log
		#self.chat = Chat(self)
	def get_players(self):
		z = []
		for id in self.players:
			p = self.players[id]
			try:
				p.username
				z.append(p)
			except:
				pass
		return z
	def msg(self, msg):
		for l in self.get_players():
			l.packetSend.chat(u'%s' % msg)
	def chat(self, player, message):
		self.log.info('<%s> %s' % (player.username, message))
		self.msg('<%s> %s' % (player.username, message))
	def join(self, player):
		self.log.info('%s has joined the game' % player.username)
		for l in self.get_players():
			l.packetSend.chat(u'\x00\xa7e%s has joined the game' % (player.username))
	def part(self, player):
		self.log.info('%s has left the game' % player.username)
		for l in self.get_players():
			l.packetSend.chat(u'\x00\xa7e%s has left the game' % (player.username))
	def setup(self):
		self.socket.bind(('0.0.0.0', self.configData['port']))
		self.socket.listen(5)
		
		self.world = World(self)
		self.world.populate()
	def close(self):
		for p in self.get_players():
			self.part(p)
			time.sleep(0.5)
			p.socket.close()
			p.abort = True
		self.socket.close()
	def listen(self):
		print "Listening for clients on port %s" % str(self.configData['port'])
		while not self.abort:
			client, addr = self.socket.accept()
			#print addr
			player = Prepare(client, addr, self.world, self)
			t = threading.Thread(target=player.listen, args=())
			t.start()
	def config(self):
		if os.path.exists('config.json'):
			f = open('config.json', 'r')
			jsondata = f.read()
			f.close()
			self.configData = json.loads(jsondata)
		else:
			jsondata = {'motd': 'A Minecraft Server... in Python!',
				'port': 25565,
				'world-path': 'world',
				'max-players': 20
			}
			self.configData = jsondata
			#self.motd = jsondata['motd']
			f = open('config.json', 'w')
			f.write(json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': ')))
			f.close()
