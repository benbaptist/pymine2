import glob, imp

class Event(list):
    """Event subscription.

    A list of callable objects. Calling an instance of this will cause a
    call to each item in the list in ascending order by index.

    Example Usage:
    >>> def f(x):
    ...     print 'f(%s)' % x
    >>> def g(x):
    ...     print 'g(%s)' % x
    >>> e = Event()
    >>> e()
    >>> e.append(f)
    >>> e(123)
    f(123)
    >>> e.remove(f)
    >>> e()
    >>> e += (f, g)
    >>> e(10)
    f(10)
    g(10)
    >>> del e[0]
    >>> e(2)
    g(2)

    """
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)

class EventManager:
    def __init__(self):
        self.chat_message_event = Event()

class PluginManager:
    def __init__(self, server):
        self.plugins = {}
        self.server = server
    
    def load_plugins(self):
        for plugin in glob.glob("plugins/*_plugin.py"):
            plugin_name = plugin[8:-10]
            self.plugins[plugin_name] = imp.load_source(plugin_name, plugin)
            getattr(self.plugins[plugin_name],plugin_name)(self.server)