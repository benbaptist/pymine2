import color_codes

def help_command(player, arguments):
    send = lambda x: player.packetSend.chat(x)
    num_args = len(arguments)

    if num_args:
        # There are arguments, so display help message.
        send("pymine2 Help")
        send("============")
        send("Welcome to pymine2, a Python-based MC server.")
        send("")
        send("To get a list of commands, please use /help.")
    else:
        # No arguments, list commands.
        send("pymine2 Commands")
        send("================")
        send("/help")
        send("/list")

def list_command(player, arguments):
    send = lambda x: player.packetSend.chat(x)
    send(str(len(player.server.get_players())) + " players online:")
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
