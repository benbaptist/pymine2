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
    def __init__(self, server, player):
        self.server = server
        self.player = player

class PlayerJoinEventHandler(list):
    def __call__(self, server, player):
        playerjoin = PlayerJoinEvent(server, player)
        for func in self:
            func(playerjoin)

class PlayerLeaveEvent:
    def __init__(self, server, player):
        self.server = server
        self.player = player

class PlayerLeaveEventHandler(list):
    def __call__(self, server, player):
        playerleave = PlayerLeaveEvent(server, player)
        for func in self:
            func(playerleave)

class PlayerMoveEvent:
    def __init__(self, server, player, x, y, z):
        self.server = server
        self.player = player
        self.x = x
        self.y = y
        self.z = z

class PlayerMoveEventHandler(list):
    def __call__(self, server, player, x, y, z):
        playermove = PlayerMoveEvent(server, player, x, y, z)
        for func in self:
            func(playermove)

class CommandEvent:
    def __init__(self, server, player, command, arguments):
        self.server = server
        self.player = player
        self.command = command
        self.arguments = arguments

class CommandEventHandler(list):
    def __call__(self, server, player, command, arguments):
        commandevent = CommandEvent(server, player, command, arguments)
        for func in self:
            func(commandevent)