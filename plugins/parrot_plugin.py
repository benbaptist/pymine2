class parrot:
    def __init__(self, server):
        self.server = server
        self.EventManager = self.server.EventManager
        self.server.log.info("Parrot plugin activated!")
        self.EventManager.chat_message_event.append(self.parrotit)
    
    def parrotit(self, player, message):
        self.server.msg("<Parrot> " + message)