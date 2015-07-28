# -*- coding: utf-8 -*-
"""
    Bot behavior
"""
from irc3 import plugin, event, rfc
from irc3.plugins.cron import cron
import random


@plugin
class Behavior(object):
    """
        Defines bot's behavior by scheduling actions or handling channel events
    """

    def __init__(self, bot):
        self.bot = bot

    # Here we can schedule something to be said or made in a specific time

    @cron('0 9 * * 1-5')
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

    @cron('0 12 * * 1-5')
    def lunch_time(self):
        """
            Say something at 12 am at work days
        """
        feeling_hungry = ['Lunch time', 'I\'m gonna get something to eat']
        to_say = random.choice(feeling_hungry)

        for channel in list(self.bot.channels):
            self.bot.privmsg(channel, to_say)

    # Here we can handle channel events to trigger something to be said or made

    @event(rfc.JOIN)
    def say_hi(self, mask=None, channel=None):
        """
            Say hi for everyone who join the channel
        """
        if self.bot.nick != mask.nick:
            # initialize greeting message
            message = '%s: Hi!' % mask.nick

            # them create Redis key that should store
            # greetings for these nick and channel
            key = 'greetings:%s:%s' % (channel.replace('#', ''), mask.nick.lower())

            # if there was at least one greeting use
            # these instead default message
            self.bot.db.SIGINT()
            greetings = self.bot.db.get(key)

            if greetings is not None:
                greeting = random.choice(greetings['greetings'].splitlines())
                message = '%s: %s' % (mask.nick, greeting)

            self.bot.privmsg(channel, message)
