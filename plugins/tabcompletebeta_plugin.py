import builtin_commands
class tabcompletebeta:
    def __init__(self, server):
        self.server = server
        self.server.EventManager.Packet_Recv_Event.append(self.tabcomplete_got)

    def tabcomplete_got(self, event):
        if event.packet["id"] == 0x14:
            text = event.packet["text"]
            last_word = text.split()[-1]
            if last_word[0] == "/":
                #It's a command.
                matching_commands = []
                for commandname in builtin_commands.command_mapping:
                    if commandname.startswith(last_word[1:]):
                        matching_commands.append(commandname)
                if matching_commands.__len__() == 1:
                    #There is only 1 command that matches.
                    event.player.packetSend.tab_complete("/" + matching_commands[0])
                elif matching_commands.__len__() > 1:
                    #There are multiple matches.
                    event.player.packetSend.tab_complete(u"\x00".join(["/" + func_name for func_name in matching_commands]))
            else:
                #It's a player name.
                matching_names = []
                for player in self.server.get_players():
                    if player.username.startswith(last_word[1:]):
                        matching_names.append(player.username)
                if matching_names.__len__() == 1:
                    #There is only 1 name that matches.
                    event.player.packetSend.tab_complete(matching_names[0])
                elif matching_names.__len__ > 1:
                    #There are multiple matches.
                    event.player.packetSend.tab_complete(u"\x00".join(matching_names))