from irc3 import plugin
from irc3.plugins.command import command
import aiohttp
import re
import random
from plugins.baseplugin import BasePlugin
from datetime import datetime, timedelta
from sqlalchemy.sql import or_


@plugin
class Commands(BasePlugin):
    """Bot commands."""
    def __init__(self, bot):
        """Initializes commands plugin.

        Args:
            bot: The running IrcBot instance.
        """
        super(Commands, self).__init__(bot)

    @command(permission='view')
    async def commit(self, mask, target, args):
        """Prints commit messages.

        %%commit
        """
        url = 'http://whatthecommit.com/index.txt'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    @command(permission='view')
    async def excuse(self, mask, target, args):
        """Prints programmers excuses.

        %%excuse
        """
        url = 'http://programmingexcuses.com'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = await response.text()

        if response:
            # Extracts the message from the HTML document.
            return re.sub(r'(^[\w\W]*<a .*?>|</a>[\w\W]*$)', '', response)

    @command(permission='view')
    async def horoscope(self, mask, target, args):
        """Prints daily horoscope.

        Signs: Aquarius, Aries, Cancer, Capricorn, Gemini,
        Leo, Libra, Pisces, Sagittarius, Scorpio, Taurus, Virgo.


        %%horoscope <sign>
        """
        zodiac_signs = [
            'Aquarius', 'Aries', 'Cancer', 'Capricorn', 'Gemini', 'Leo',
            'Libra', 'Pisces', 'Sagittarius', 'Scorpio', 'Taurus', 'Virgo'
        ]
        wished = (args.get('<sign>') or '').capitalize()
        if wished not in zodiac_signs:
            return f'{wished} is not a valid sign.'

        url = f'http://horoscope-api.herokuapp.com/horoscope/today/{wished}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = await response.json()

        msg = 'I\'m sorry but the stars seems to be unreachable.'
        if response:
            horoscope = response.get('horoscope', '')
            if horoscope:
                msg = horoscope

        return msg

    @command(permission='admin')
    async def greeting(self, mask, target, args):
        """Saves a new greeting message to a specific nick.

        %%greeting <nick> <message>...
        """
        try:
            table = self.bot.dataset['greetings']
            channel = target.replace('#', '')
            nick = args['<nick>'].lower()
            message = ' '.join(args['<message>'])
            result = table.find_one(channel=channel, nick=nick) or {}
            options = '\n'.join([result.get('options', ''), message])
            table.upsert({
                'channel': channel,
                'nick': nick,
                'options': options,
            }, ['channel', 'nick'])

            return 'Okie dokie'
        except Exception:
            return 'Sorry, looks like something went wrong :('

    @command(permission='view')
    async def joke(self, mask, target, args):
        """Prints a Joke.

        You can also pass a subject for an especific kind of joke.
        The available subjects are: 'chuck norris', and 'yo momma'

        %%joke [<subject>...]
        """
        jokes_api = {
            'icndb': 'http://api.icndb.com/jokes/random?escape=javascript',
            'yomomma': 'http://api.yomomma.info/',
        }
        subject = None
        if '<subject>' in args and len(args['<subject>']) > 0:
            subject_list = [s.lower() for s in args['<subject>']]
            subject = ' '.join(subject_list)
        url = None

        if subject == 'chuck norris':
            url = jokes_api['icndb']
        elif subject == 'yo momma':
            url = jokes_api['yomomma']
        else:
            url = random.choice(list(jokes_api.values()))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.json(content_type=None)

            # There are two different possible structures for the
            # response, one has a `joke` field at the response root,
            # and the other one has the `joke` field inside an element
            # cablled `value`, so we must try both in order to
            # reach the text.
            if type(response) is dict:
                if 'joke' in response:
                    return response['joke']
                elif ('value' in response
                      and type(response['value']) is dict
                      and 'joke' in response['value']):
                    return response['value']['joke']

            # No joke? That it is really sad :(
            raise Exception('No joke found')

        except Exception as e:
            print(e)
            return 'All work and no play makes Jack a dull boy'

    @command(permission='view')
    async def cebolate(self, mask, target, args):
        """Prints message translated to Cebolinha's dialect.

        %%cebolate <message>...
        """
        msg = ' '.join((args.get('<message>') or [])).strip()
        if msg:
            return msg.replace('R', 'L').replace('r', 'l')

    @command(permission='view')
    async def urls(self, mask, target, args):
        """Returns channel URLs history.

        There are two arguments available for filtering.

        date: It can be today, yesterday, week, month
        or an ISO date (YYYY-mm-dd).

        keyword: Any word present in the page title
        you are looking for.

        %%urls [<date> [<keyword>...]]
        """
        table = self.bot.dataset['url_history'].table
        statement = table.select().where(
            table.c.channel == target.replace('#', '')
        )

        date = (args.get('<date>') or '').lower()
        if date:
            # regular expression for ISO dates
            regex = (
                r'^([12]\d{3})-(0[1-9]|1[012])-(0[1-9]|[12]\d|3[01])'
                r'( (0\d|1\d|2[0-3]):(0\d|[1-5]\d)(:(0\d|[1-5]\d))?)?$'
            )

            # initializes the interval with the current day, aka today :P
            b = {'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0}
            e = {'hour': 23, 'minute': 59, 'second': 59, 'microsecond': 999999}
            bd = datetime.utcnow()
            bd = bd.replace(**b)  # begin date
            ed = bd.replace(**e)  # end date

            if date == 'yesterday':
                bd -= timedelta(1)
                ed -= timedelta(1)
            elif date == 'week':
                bd -= timedelta(days=bd.weekday())
            elif date == 'month':
                bd = bd.replace(day=1)
            elif re.match(regex, date):
                try:
                    bd = datetime.fromisoformat(date)
                except ValueError:
                    self.bot.privmsg(target, 'Invalid date')
                    return
                bd = bd.replace(**b)
                ed = bd.replace(**e)
            elif date != 'today':
                bd, ed = None, None

            if bd and ed:
                statement = statement.where(
                    table.c.datetime >= bd
                ).where(
                    table.c.datetime <= ed
                )

        keywords = args.get('<keyword>', [])
        if keywords:
            likes = [table.c.title.ilike(f'%{word}%') for word in keywords]
            statement = statement.where(or_(*likes))

        statement = statement.order_by(-table.c.datetime).limit(5)
        result = self.bot.dataset.query(statement)

        for item in result:
            _dt = item.get('datetime').strftime('%Y-%m-%d')
            _url = item.get('url')
            _title = item.get('title', '')
            msg = f'{_dt} {_url} [{_title}]'
            self.bot.privmsg(target, msg)

    @command(permission='view')
    async def slackers(self, mask, target, args):
        """Prints channel's slackers rank.

        %%slackers
        """
        table = self.bot.dataset['slackers']
        result = table.find(channel=target, order_by='-words') or []
        rank = [f'{row["nick"]} ({row["words"]})' for row in result]
        self.bot.privmsg(target, ', '.join(rank))

    @command(permission='view')
    async def karma(self, mask, target, args):
        """Prints channel's karma list.

        %%karma
        """
        table = self.bot.dataset['karma']
        result = table.find(channel=target, order_by='-status') or []
        karmas = [f'{row["entity"]} ({row["status"]})' for row in result]
        self.bot.privmsg(target, ', '.join(karmas))
