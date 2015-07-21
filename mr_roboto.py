# -*- coding: utf-8 -*-
from irc3 import IrcBot
from decouple import config


def main():
    # load bot settings
    settings = dict(
        nick=config('nick'),
        autojoins=config('autojoins', cast=lambda v: [s.strip().strip('\\') for s in v.split('\n') if s]),
        host=config('host'),
        port=config('port', cast=int),
        ssl=config('ssl', cast=bool),
        includes=config('includes', cast=lambda v: [s.strip() for s in v.split('\n') if s])
    )
    # start bot
    bot = IrcBot.from_config(settings)
    bot.run(forever=True)

if __name__ == '__main__':
    main()
