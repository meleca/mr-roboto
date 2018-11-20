# -*- coding: utf-8 -*-


class BasePlugin:
    """
        Base plugin class.
    """
    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def reload(cls, old):
        print(f'reloading plugin {cls.__name__}')
        return cls(old.bot)
