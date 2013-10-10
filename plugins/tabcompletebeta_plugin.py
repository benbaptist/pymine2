#Not finished yet. I will finish that after my vacation.
import builtin_commands
class tabcompletebeta:
    def __init__(self, server):
        self.server = server
        self.server.EventManager.Packet_Recv_Event.append(self.tabcomplete_got)
    
    def tabcomplete_got(self, event):
        if event.packet["id"] == 0xCB:
            text = event.packet["text"]
            if text[0] == "/":
                #It's a command.
                matching_commands = []
                for commandname in builtin_commands.command_mapping:
                    if commandname.startswith(text[1:]):
                        matching_commands.append(commandname)
                if matching_commands.__len__():
                    #There is only 1 command that matches.
                    event.player.packetSend.tab_complete(matching_commands[0])