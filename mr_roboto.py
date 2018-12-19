from os import path
from config import conf
from irc3 import IrcBot
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re


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


def get_version_from_file(filename):
    """Tries to get bot's version number originally stored on Makefile."""
    regex = re.compile(r'VERSION = (\d+.\d+.\d+)$')
    match = None

    try:
        with open(filename) as vfile:
            for line in vfile:
                match = regex.match(line)
                if match:
                    break
    except OSError as err:
        print(f'Failed to open Makefile: {err.strerror}')

    return match.group(1) if match else '?.?.?'


def main():
    """Initializes a new irc3 bot."""
    bot = IrcBot.from_config(conf)
    bot.version = get_version_from_file('Makefile')
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
