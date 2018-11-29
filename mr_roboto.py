from os import path
from config import conf
from irc3 import IrcBot
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ReloadEventHandler(FileSystemEventHandler):
    """Handles auto reload whenever a plugin source code changes."""
    def __init__(self, bot, config):
        """Initializes the handler with the following arguments.

        Args:
            bot: The IrcBot instance that must be reloaded.
            config: The configuration set used to initialize the bot.
        """
        self.bot = bot
        self.config = config

    def on_modified(self, event):
        """Called whenever a file or directory is modified.

        Args:
            event: Event representing the modified file or directory.
        """
        super(ReloadEventHandler, self).on_modified(event)

        if (event.src_path.endswith('.py') and
                path.dirname(event.src_path).endswith('plugins')):
            local_plugins = filter(lambda lp: lp.startswith('plugins'),
                                   self.config['includes'])
            self.bot.reload(*local_plugins)


def main():
    """Initializes a new irc3 bot."""
    bot = IrcBot.from_config(conf)

    observer = Observer()
    observer.schedule(
        ReloadEventHandler(bot, conf),
        path.dirname(path.abspath(__file__)),
        recursive=True
    )
    observer.start()

    try:
        bot.run(forever=True)
    except KeyboardInterrupt:
        observer.stop()


if __name__ == '__main__':
    main()
