import socket, threading, os, json, random, string, time, color_codes, plugin
from player import Player
from player import Prepare
from world import World
from chat import Chat
from config import Config

class Server:
	def __init__(self, log):
		self.socket = socket.socket()
		self.abort = False
		self.players = {}
		self.log = log
		self.config = Config(log).config
		self.EventManager = plugin.EventManager()
		self.PluginManager = plugin.PluginManager(self)
		self.PluginManager.load_plugins()
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
	def find_player(self, username):
		for pl in self.get_players():
			if pl.username == username:
				return pl
	def msg(self, msg):
		color_coded_msg = color_codes.replace_color_codes(msg)
		for l in self.get_players():
			l.packetSend.chat(u'%s' % color_coded_msg)
	def chat(self, player, message):
		message = self.EventManager.Chat_Message_Event(self, player, message)
		self.log.info('<%s> %s' % (player.username, message))
		self.msg('<%s> %s' % (player.username, message))
	def join(self, player):
		self.log.info('%s has joined the game' % player.username)
		self.EventManager.Player_Join_Event(self, player)
		for l in self.get_players():
			if l.username == player.username:
				continue
			l.packetSend.player_list_item(player.username, True, 0)
			l.packetSend.chat(u'\x00\xa7e%s has joined the game' % (player.username))
	def part(self, player):
		self.log.info('%s has left the game' % player.username)
		for l in self.get_players():
			if l.username == player.username:
				continue
			l.packetSend.player_list_item(player.username, False, 0)
			l.packetSend.chat(u'\x00\xa7e%s has left the game' % (player.username))
	def setup(self):
		self.socket.bind(('0.0.0.0', self.config['port']))
		self.socket.listen(5)
		
		self.world = World(self, self.config['world-path'])
		self.world.populate()
		t = threading.Thread(target=self.world.loop, args=())
		t.start()
	def close(self):
		for p in self.get_players():
			p.disconnect('Server going down')
		self.socket.close()
		self.abort = True
		self.world.flush()
	def listen(self):
		self.log.info("Listening for clients on port %s" % str(self.config['port']))
		while not self.abort:
			client, addr = self.socket.accept()
			#print addr
			player = Prepare(client, addr, self.world, self)
			t = threading.Thread(target=player.listen, args=())
			t.start()
