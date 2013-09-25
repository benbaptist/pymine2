import glob, imp
import events

class EventManager:
    def __init__(self):
        self.Chat_Message_Event = events.ChatMessageEventHandler()
        self.Player_Join_Event = events.PlayerJoinEventHandler()
        self.Player_Move_Event = events.PlayerMoveEventHandler()

class PluginManager:
    def __init__(self, server):
        self.plugins = {}
        self.server = server
    
    def load_plugins(self):
        for plugin in glob.glob("plugins/*_plugin.py"):
            plugin_name = plugin[8:-10]
            self.plugins[plugin_name] = imp.load_source(plugin_name, plugin)
            getattr(self.plugins[plugin_name],plugin_name)(self.server)