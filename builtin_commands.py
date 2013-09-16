import color_codes

def help_command(player, arguments):
    send = lambda x: player.packetSend.chat(x)
    
    if len(arguments):
        send("pymine2 Commands")
        send("================")
        send("/help")
        send("/list")
    else:
        send("pymine2 Help")
        send("============")
        send("Welcome to pymine2, a lightweight Minecraft Python server")
        send("that can run on mobile devices.")
        send("")
        send("To get a list of commands, please type /help commands in the chat.")

def list_command(player, arguments):
    send = lambda x: player.packetSend.chat(x)
    
    send(",".join( [pl.username for pl in player.server.get_players()] ))

command_mapping = {
"help": help_command,
"list": list_command
}

def run_command(player, command, arguments):
    try:
        command_mapping[command](player, arguments)
    except Exception, e:
        player.packetSend.chat("Error while running command!")
        print e
