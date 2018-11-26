class BasePlugin:
    """Base plugin class.

    Describes common behavior and attributes between plugins.
    """
    def __init__(self, bot):
        """Initializes the base plugin.

        Args:
            bot: The running IrcBot instance.
        """
        self.bot = bot

    @classmethod
    def reload(cls, old):
        """Reloads plugin.

        This method is called whenever the plugin source code
        is modified.

        Args:
            old: The current plugin instance.
        """
        print(f'reloading plugin {cls.__name__}')
        return cls(old.bot)
