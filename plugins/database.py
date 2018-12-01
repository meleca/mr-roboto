import dataset
from irc3 import plugin
from plugins.baseplugin import BasePlugin


@plugin
class Database(BasePlugin):
    """Interface to access bot's database.

    For usage take a look at dataset documentation.
    For database support take a look at SQLAlchemy documentation.
    """
    def __init__(self, bot):
        """Initializes database plugin.

        Args:
            bot: The running IrcBot instance.
        """
        super(Database, self).__init__(bot)
        self.bot.dataset = dataset.connect(self.bot.config.database)
