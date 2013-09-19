import server, time, Queue, threading
class PymineLogger:
	def __init__(self):
		self.file = open('server.log', 'a')
		self.abort = False
		self.log_queue = Queue.Queue()
		threading.Thread(target=self.process_queue, args=()).start()
	
	def error(self, i):
		line = u'[%s] [ERROR] %s' % (str(time.time()), i)
		self.log_queue.put(line)
	
	def info(self, i):
		line = u'[%s] [INFO] %s' % (str(time.time()), i)
		self.log_queue.put(line)
	
	def process_queue(self):
		while not self.abort:
			try:
				log_line = self.log_queue.get(timeout=1)
				print log_line
				self.file.write("%s\n" % log_line)
				self.file.flush()
			except Queue.Empty:
				pass
	
	def stop(self):
		self.abort = True

log = PymineLogger()

server = server.Server(log)
server.setup()
try:
	server.listen()
except KeyboardInterrupt:
	log.info("Gracefully terminating")
	log.stop()
	server.close()