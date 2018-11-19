# -*- coding: utf-8 -*-
"""
    Bot database interface
"""
import dataset
from irc3 import plugin


@plugin
class Database(object):
    """
    Interface to access bot's database.

    For usage take a look at dataset documentation.
    For database support take a look at SQLAlchemy documentation.
    """
    def __init__(self, context):
        """
        Initializes database plugin.

        Args:
            context (irc3.IrcBot): The running IrcBot instance.
        """
        self.context = context
        self.context.db = dataset.connect(self.context.config.database)
