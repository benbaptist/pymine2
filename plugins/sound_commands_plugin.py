class sound_commands:
    def __init__(self, server):
        self.server = server
        self.EventManager = server.EventManager
        server.log.info("SoundCommands Plugin Started")
        self.EventManager.Command_Event.append(self.play_sound_here)
    
    def play_sound_here(self, event):
        if event.command == "playsoundhere":
            event.player.packetSend.named_sound_effect(event.arguments[0], event.player.x, event.player.y, event.player.z)