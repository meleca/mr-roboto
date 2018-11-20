# -*- coding: utf-8 -*-
"""
    Bot behavior
"""
from irc3 import plugin, event, rfc
from irc3.plugins.cron import cron
from lxml import html
import aiohttp
import random
import re
from . import BasePlugin


@plugin
class Behaviors(BasePlugin):
    """
        Defines bot's behavior by scheduling
        actions or handling channel events.
    """
    def __init__(self, bot):
        super(Behaviors, self).__init__(bot)

        # List of rules for channel messages
        # Each item has a tuple containing an RE and a reference to the
        # procedure to be executed
        self.channel_rules = self.compile_rules([
            ('(https?://[^ \t>\n\r\x01-\x1f]+)', self.handle_url),
        ])

    def compile_rules(self, rules):
        """
            Compile a list of RE and return a new list with
            each RE compiled and its procedure reference
        """
        if type(rules) is list:
            return [(re.compile(rule, re.UNICODE), func)
                    for (rule, func) in rules]
        else:
            return None

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
            message = '%s: Hi!' % mask.nick
            channel = channel.replace('#', '')
            nick = mask.nick.lower()
            table = self.bot.dataset['greetings']
            result = table.find_one(channel=channel, nick=nick) or {}

            if result.get('options', ''):
                greeting = random.choice(result['options'].splitlines())
                message = '%s: %s' % (mask.nick, greeting)

            self.bot.privmsg(channel, message)

    @event(rfc.PRIVMSG)
    async def handle_message(self, mask=None, event=None, target=None, data=None):
        """
            Handle channel messages
        """
        if self.channel_rules and type(self.channel_rules) is list:

            try:
                # Check channel rules looking for some nice interaction
                # If at least one rule match with the channel message execute
                # it's callback
                for rule, func in self.channel_rules:
                    match = rule.search(data)
                    if match:
                        await func(target, match.group(1).encode('utf-8'))

            except Exception as e:
                print(e)
                self.bot.privmsg(target, 'Booom shakalaka')

    async def handle_url(self, target, url):
        """
            Load URL address and send its web page title back to the
            channel
        """
        # MIME Type Handling functions
        def handle_text(target, subtype, data, charset):
            try:
                content = str(data, encoding=charset)
            except UnicodeDecodeError as e:
                # It's still possible that part of the site processing changes
                # the encoding (i.e. ascii animations). Hence we try to find the
                # title within the range with correct charset
                content = str(data[:e.end-1], encoding=charset)

            page = html.fromstring(content)
            title = page.findtext('.//title')

            if title is not None:
                self.bot.privmsg(target, ('[%s]' % title.strip()))

        def handle_image(target, subtype, data):
            self.bot.privmsg(target, 'Looks like an image')

        def handle_audio(target, subtype, data):
            self.bot.privmsg(target, 'Do you know I\'m deaf right?')

        def handle_video(target, subtype, data):
            self.bot.privmsg(target, 'For God sake I\'m blind')

        def handle_default(target, subtype, data):
            self.bot.privmsg(target, 'What kind of weed is that?')

        # MIME Type dict
        type_handlers = {
            u'text': handle_text,
            u'image': handle_image,
            u'audio': handle_audio,
            u'video': handle_video
        }

        # First of all load the page
        async with aiohttp.ClientSession() as session:
            async with session.get(url.decode('utf-8')) as request:
                # Extract mime type
                rule = re.compile('^(\w+)/([\w\-\+]+)( *;.*)?$')
                match = rule.search(request.headers['CONTENT-TYPE'])
                if not match:
                    self.bot.privmsg(
                        target,
                        'My sources say that this links does not exists')
                    return

                mime_type = match.group(1)
                subtype = match.group(2)

                # Then parses its HTML and search for the title
                data = await request.read()

        # Handle content
        if mime_type in type_handlers:
            if mime_type == u'text':
                type_handlers[mime_type](target, subtype, data, request.charset)
            else:
                type_handlers[mime_type](target, subtype, data)
        else:
            self.handle_default(target, subtype, data)
