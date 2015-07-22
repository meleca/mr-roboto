# -*- coding: utf-8 -*-
"""
    commit
"""
from irc3 import plugin
from irc3.plugins.command import command
import asyncio
import aiohttp


@plugin
class Commits(object):
    """
    Commands that prints Commit Messages
    """

    def __init__(self, bot):
        self.bot = bot

    @command(permission='view')
    @asyncio.coroutine
    def commit(self, mask, target, args):
        """
            Commit

            %%commit
        """
        request = yield from aiohttp.request('GET', 'http://whatthecommit.com/index.txt')
        return (yield from request.text())
