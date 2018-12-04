from irc3 import plugin, event, rfc
from irc3.plugins.cron import cron
from lxml import html
import aiohttp
import random
import re
from plugins.baseplugin import BasePlugin
from datetime import datetime


@plugin
class Behaviors(BasePlugin):
    """Bot behavior.

    Defines bot's behavior by scheduling actions
    or handling channel events.
    """
    def __init__(self, bot):
        """Initializes behavior plugin.

        Args:
            bot: The running IrcBot instance.
        """
        super(Behaviors, self).__init__(bot)

        # List of rules for channel's messages.
        # Each item has a tuple containing
        # an RE and a reference to the
        # method to be executed.
        self.channel_rules = self._compile_rules([
            (r'(https?://[^ \t>\n\r\x01-\x1f]+)', self.handle_url),
        ])

    def _compile_rules(self, rules):
        """Plugin rules compiler.

        Compiles a list of RE and return a new list with
        each RE compiled and its method reference.

        Args:
            rules: List of rules for channel's messages.
        """
        if type(rules) is list:
            return [(re.compile(rule, re.UNICODE), func)
                    for (rule, func) in rules]
        else:
            return None

    @cron('0 9 * * 1-5')  # week-days 9am
    def good_morning(self):
        """Says something in the morning.

        Automatic sends a random message every week day 9am.
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

    @cron('0 12 * * 1-5')  # week-days 12pm
    def lunch_time(self):
        """Say something at noon.

        Automatic sends a random message every week day 12pm.
        """
        feeling_hungry = ['Lunch time', 'I\'m gonna get something to eat']
        to_say = random.choice(feeling_hungry)

        for channel in list(self.bot.channels):
            self.bot.privmsg(channel, to_say)

    @event(rfc.JOIN)
    def say_hi(self, mask=None, channel=None):
        """Greets everyone who joins the channel.

        Args:
            mask: An IrcString containing useful information.
            channel: Channel name.
        """
        if self.bot.nick != mask.nick:
            message = f'{mask.nick}: Hi!'
            nick = mask.nick.lower()
            table = self.bot.dataset['greetings']
            result = table.find_one(channel=channel.replace('#', ''),
                                    nick=nick) or {}

            if result.get('options', ''):
                greeting = random.choice(result['options'].splitlines())
                message = f'{mask.nick}: {greeting}'

            self.bot.privmsg(channel, message)

    @event(rfc.PRIVMSG)
    async def handle_message(self, mask=None, event=None, target=None,
                             data=None):
        """Handles channel's messages.

        Args:
            mask: An IrcString containing useful information.
            event: The IRC event, it can be PRIVMSG or NOTICE.
            target: Channel name.
            data: The message sent to the channel.
        """
        if self.channel_rules and type(self.channel_rules) is list:

            try:
                # Verifies if any rule match with the given text message,
                # if it does, executes its callback.
                for rule, func in self.channel_rules:
                    match = rule.search(data)
                    if match:
                        await func(target, match.group(1).encode('utf-8'))

            except Exception as e:
                print(e)
                self.bot.privmsg(target, 'Booom shakalaka')

    async def handle_url(self, target, url):
        """Handler for URLs.

        Attempts to load the URL address, if no problem occur
        it checks the response in order to validate its type
        and send the page title back to the channel if available.
        At the end updates the URLs history.

        Args:
            target: Channel name.
            url: A valid URL.
        """
        history = {
            'channel': target.replace('#', ''),
            'url': url.decode('utf-8'),
            'title': '',
            'datetime': datetime.utcnow()
        }

        def handle_text(target, subtype, data, charset='utf-8'):
            try:
                content = str(data, encoding=charset)
            except UnicodeDecodeError as e:
                # It's still possible that part of the site processing changes
                # the encoding (i.e. ascii animations). Hence we try to find
                # the title within the range with correct charset.
                try:
                    content = str(data[:e.end-1], encoding=charset)
                except UnicodeDecodeError:
                    # If it fails again, just forget it and return.
                    self.bot.privmsg(
                        target,
                        '... it seems this site has a pretty broken charset')
                    return

            page = html.fromstring(content)
            title = page.findtext('.//title')

            if title:
                history['title'] = title.strip()
                self.bot.privmsg(target, f'[{history.get("title")}]')

        def handle_image(target, subtype, data):
            self.bot.privmsg(target, 'Looks like an image')

        def handle_audio(target, subtype, data):
            self.bot.privmsg(target, 'Do you know I\'m deaf right?')

        def handle_video(target, subtype, data):
            self.bot.privmsg(target, 'For God sake I\'m blind')

        def handle_default(target, subtype, data):
            self.bot.privmsg(target, 'What kind of weed is that?')

        type_handlers = {
            u'text': handle_text,
            u'image': handle_image,
            u'audio': handle_audio,
            u'video': handle_video
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url.decode('utf-8')) as request:
                # Extract mime type.
                rule = re.compile(r'^(\w+)/([\w\-\+]+)( *;.*)?$')
                match = rule.search(request.headers['CONTENT-TYPE'])
                if not match:
                    self.bot.privmsg(
                        target,
                        'My sources say that this links does not exists')
                    return

                mime_type = match.group(1)
                subtype = match.group(2)
                data = await request.read()

        if mime_type in type_handlers:
            if mime_type == u'text' and request.charset:
                type_handlers[mime_type](target, subtype, data,
                                         request.charset)
            else:
                type_handlers[mime_type](target, subtype, data)
        else:
            handle_default(target, subtype, data)

        table = self.bot.dataset['url_history']
        table.upsert(history, ['channel', 'url'])
