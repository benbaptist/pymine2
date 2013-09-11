import server, time
class Log:
	def __init__(self):
		self.file = open('server.log', 'a')
	def error(self, i):
		line = u'[%s] [ERROR] %s' % (str(time.time()), i)
		print line
		self.file.write(u'%s\n' % line)
		self.file.flush()
	def info(self, i):
		line = u'[%s] [INFO] %s' % (str(time.time()), i)
		print line
		self.file.write(u'%s\n' % line)
		self.file.flush()
log = Log()

server = server.Server(log)
server.config()
server.setup()
try:
	server.listen()
except KeyboardInterrupt:
	print "Gracefully terminating"
	server.close()