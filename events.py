class GenericEventHandler(list):
    def __call__(self, *args, **kwargs):
        for func in self:
            func(args, kwargs)

class ChatMessageEvent:
    def __init__(self, server, player, message):
        self.server = server
        self.player = player
        self.message = message

class ChatMessageEventHandler(list):
    def __call__(self, server, player, message):
        chatmessage = ChatMessageEvent(server, player, message)
        for func in self:
            func(chatmessage)
        return chatmessage.message

class PlayerJoinEvent:
    def __init__(self, server, jointime, player):
        self.server = server
        self.jointime = jointime
        self.player = player

class PlayerJoinEventHandler(list):
    def __call__(self, server, jointime, player):
        playerjoin = PlayerJoinEvent(server, jointime, player)
        for func in self:
            func(playerjoin)