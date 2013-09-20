import color_codes

def help_command(player, arguments):
	send = lambda x: player.packetSend.chat(x)
	num_args = len(arguments)

	if not num_args:
		# No arguments, show general help.
		send("pymine2 Help")
		send("============")
		send("Welcome to pymine2, a Python-based MC server.")
		send("")
		send("To get a list of commands, please use /help commands.")
	else:
		# There are arguments, so do a subcommand
		if arguments[0] == "commands":
				send("pymine2 Commands")
				send("================")
				send("/help")
				send("/list")
				send("/msg targetName message")
		else:
				send("No such subcommand!")
def list_command(player, arguments):
	send = lambda x: player.packetSend.chat(x)
	send(str(len(player.server.get_players())) + " players online:")
	send(",".join( [pl.username for pl in player.server.get_players()] ))

def msg_command(player, arguments):
	message = " ".join(arguments[1:])
	target = player.server.find_player(arguments[0])
	if target:
		target.packetSend.chat(color_codes.yellow + player.username + " whispers to you: " + color_codes.white + message)
	else:
		player.packetSend.chat(color_codes.red + "No such player " + arguments[0] + "!")
def time(player, arguments):
	if arguments[0] == "set":
		try:
			desired_time = arguments[1].replace("day", str(0)).replace("night", str(12500))
			tick = int(desired_time)
			player.server.world.level['time'] = tick
		except Exception, e:
			player.server.log.error(e)
			player.packetSend.chat(color_codes.red + "Invalid time!")
	elif arguments[0] == "add":
		try:
			tick = int(arguments[1])
			player.server.world.level['time'] += tick
		except:
			player.packetSend.chat(color_codes.red + "Invalid time!")

command_mapping = {
	"help": help_command,
	"list": list_command,
	"msg": msg_command,
	"time": time
}

def run_command(player, command, arguments):
	try:
		command_mapping[command](player, arguments)
	except Exception, e:
		player.packetSend.chat("Error while running command!")
		print e
