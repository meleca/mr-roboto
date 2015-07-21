# -*- coding: utf-8 -*-
from irc3 import IrcBot, utils
import sys


def main():
    # parse configs
    if len(sys.argv) != 2:
        print('Usage: mr_roboto <settings_file>')
    config = utils.parse_config('bot', sys.argv[1])
    # start bot
    bot = IrcBot.from_config(config)
    bot.run(forever=True)

if __name__ == '__main__':
    main()
