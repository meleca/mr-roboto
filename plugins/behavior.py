# -*- coding: utf-8 -*-
"""
    Bot behavior
"""
from irc3 import plugin
from irc3.plugins.cron import cron
import random

@plugin
class Behavior(object):
    """
        Defines bot's behavior by scheduling actions or handling channel events
    """

    def __init__(self, bot):
        self.bot = bot

    ### Here we can schedule something to be said or made in a specific time ###

    @cron('* 9 * * 1-5')
    def good_morning(self):
        """
            Says something in the morning at work days
        """
        feeling_sleepy = [
            'Good morning',
            'Good morning fellas',
            'Morning',
            'Hello everyone',
            'I definitely need a coffee. Oh, hello btw.'
        ]
        to_say = random.choice(feeling_sleepy)

        for channel in list(self.bot.channels):
            self.bot.privmsg(channel, to_say)

    @cron('* 12 * * 1-5')
    def lunch_time(self):
        """
            Say something at 12 am at work days
        """
        feeling_hungry = ['Lunch time', 'I\'m gonna get something to eat']
        to_say = random.choice(feeling_hungry)

        for channel in list(self.bot.channels):
            self.bot.privmsg(channel, to_say)
