import color_codes

class welcome:
    def __init__(self, server):
        self.server = server
        self.EventManager = server.EventManager
        server.log.info("Welcome plugin activated!")
        server.EventManager.Player_Join_Event.append(self.welcome)
    
    def welcome(self, event):
        event.player.packetSend.chat(color_codes.yellow + "Hello %s! Welcome to our server." % event.player.username)