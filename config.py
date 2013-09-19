import json, os
class Config:
	def __init__(self, log):
		self.log = log
		if os.path.exists('config.json'):
			f = open('config.json', 'r')
			self.config = json.loads(f.read())
			f.close()
		else:
			self.log.info('config.json does not exist, creating')
			self.config = {}
		self.check()
	def check(self): # ensure config.json has all of the configuration settings
		defaults = {'motd': '',
				'port': 25565,
				'world-path': 'world',
				'max-players': 20,
				'gamemode': 0,
				'server-name': 'A Minecraft Server... in Python!'
			}
		if 'server-name' not in self.config and 'motd' in self.config:
			self.log.info('Renaming config entry motd to server-name...')
			self.config['server-name'] = self.config['motd']
			self.config['motd'] = ''
		for key in defaults:
			if key not in self.config:
				self.log.info('%s not in config.json, setting to default value: "%s"' % (key, defaults[key]))
				self.config[key] = defaults[key]
		self.flush()
	def flush(self):
		f = open('config.json', 'w')
		f.write(json.dumps(self.config, sort_keys=True, indent=4, separators=(',', ': ')))
		f.close()