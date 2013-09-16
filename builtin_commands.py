import color_codes

def help_command(player, arguments):
    send = lambda x: player.packetSend.chat(x)
    num_args = len(arguments)

    if not num_args:
        # No arguments, list commands.
        send("pymine2 Help")
        send("============")
        send("Welcome to pymine2, a Python-based MC server.")
        send("")
        send("To get a list of commands, please use /help commands.")
    else:
        # There are arguments, so display help message.
        send("pymine2 Commands")
        send("================")
        send("/help")
        send("/list")
        send("/msg targetName message")

def list_command(player, arguments):
    send = lambda x: player.packetSend.chat(x)
    send(str(len(player.server.get_players())) + " players online:")
    send(",".join( [pl.username for pl in player.server.get_players()] ))

def msg_command(player, arguments):
    message = " ".join(arguments[1:])
    player.server.find_player(arguments[0]).packetSend.chat(color_codes.yellow + player.username + " whispers to you: " + color_codes.white + message)

command_mapping = {
"help": help_command,
"list": list_command,
"msg": msg_command
}

def run_command(player, command, arguments):
    try:
        command_mapping[command](player, arguments)
    except Exception, e:
        player.packetSend.chat("Error while running command!")
        print e
