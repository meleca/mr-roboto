# -*- coding: utf-8 -*-
"""
    Bot commands
"""
from irc3 import plugin
from irc3.plugins.command import command
import aiohttp
import re
import random
import json
from . import BasePlugin
from datetime import datetime, timedelta
from sqlalchemy.sql import or_


@plugin
class Commands(BasePlugin):
    """
        Handle commands called by users.
    """
    def __init__(self, bot):
        super(Commands, self).__init__(bot)

    @command(permission='view')
    async def commit(self, mask, target, args):
        """
            Prints Commit Messages

            %%commit
        """
        url = "http://whatthecommit.com/index.txt"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    @command(permission='view')
    async def excuse(self, mask, target, args):
        """
            Prints Programmer Excuses

            %%excuse
        """
        url = "https://api.githunt.io/programmingexcuses"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    @command(permission='view')
    async def horoscope(self, mask, target, args):
        """
            Prints daily horoscope (pt_br only)

            %%horoscope <zodiac>
        """
        wished = args['<zodiac>']

        # list of zodiacs and a regular expression matching its names
        # this will be used to identify what zodiac user is looking for
        zodiac_table = {
            u'\u00c1ries': u'[A\u00c1a\u00e1]ries',
            u'Touro': u'[Tt]ouro',
            u'G\u00eameos': u'[Gg][\u00eae]meos',
            u'C\u00e2ncer': u'[Cc][\u00e2a]ncer',
            u'Le\u00e3o': u'[Ll]e[\u00e3a]o',
            u'Virgem': u'[Vv]irgem',
            u'Libra': u'[Ll]ibra',
            u'Escorpi\u00e3o': u'[Ee]scorpi[\u00e3a]o',
            u'Sagit\u00e1rio': u'[Ss]agit[\u00e1a]rio',
            u'Capric\u00f3rnio': u'[Cc]apric[\u00f3o]rnio',
            u'Aqu\u00e1rio': u'[Aa]qu[\u00e1a]rio',
            u'Peixes': u'[Pp]eixes'
        }

        # default answer
        msg = 'Os astros parecem confusos, e eu mais ainda'

        # the horoscopo API service provides daily information about horoscope
        url = "http://developers.agenciaideias.com.br/horoscopo/json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response = await response.json(content_type=None)

        if response and 'signos' in response:
            the_one = None
            for zodiac_name, zodiac_regex in zodiac_table.items():
                if re.match(zodiac_regex, wished):
                    the_one = zodiac_name
                    break
            if not the_one:
                return (u'%s n\u00e3o consta nos meus mapas astrais' % wished)
            else:
                for zodiac in response['signos']:
                    if zodiac['nome'] == the_one:
                        zmsg = zodiac['msg']
                        zmsg = zmsg.replace('\r', '')
                        zmsg = zmsg.replace('\n', '')
                        zmsg = zmsg.replace('\t', '')
                        if zmsg:
                            msg = zmsg
                        break
        return msg

    @command(permission='admin')
    async def greeting(self, mask, target, args):
        """
            Save new greeting message to a specific nick

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
        except Exception as e:
            return 'Sorry, looks like something went wrong :('

    @command(permission='view')
    async def joke(self, mask, target, args):
        """
            Prints a Joke.
            You can also pass a subject for an especific kind of joke.
            The available subjects are:
                chuck norris,
                yo momma

            %%joke [<subject>...]
        """
        # List of available APIs
        jokes_api = {
            'icndb': 'http://api.icndb.com/jokes/random?escape=javascript',
            'yomomma': 'http://api.yomomma.info/',
        }

        # Check if there is some subject
        subject = None
        if '<subject>' in args and len(args['<subject>']) > 0:
            # Convert subjects to a single lower case string
            subject_list = [ s.lower() for s in args['<subject>'] ]
            subject = ' '.join(subject_list)

        # Choose one API to request
        url = None

        if subject == 'chuck norris':
            # Pick one from icndb API
            url = jokes_api['icndb']
        elif subject == 'yo momma':
            # Pick one from yo momma API
            url = jokes_api['yomomma']
        else:
            # Pick a random source
            url = random.choice(list(jokes_api.values()))

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response = await response.json(content_type=None)

            # There is two different structure possible for the response
            # one has a 'joke' field at the response root
            # the other one the 'joke' field is inside an element called 'value'
            # so we must try both
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
        """
            Prints message translated to Cebolinha's dialect

            %%cebolate <message>...
        """
        method = 'POST'
        url = 'http://cebolatol.julianofernandes.com.br/api/tlanslate'
        payload = {'message': ' '.join(args['<message>'])}
        headers = {'content-type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(payload),
                                    headers=headers) as response:
                response = await reponse.json()

        if type(response) is dict:
            if 'phlase' in response:
                return response['phlase']
            elif 'ellol' in response:
                return response['ellol']

        return 'Sorry, something went wlong'

    @command(permission='view')
    async def urls(self, mask, target, args):
        """
            Returns channel URLs history.

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
                    return 'Invalid date'
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
            msg = '%s %s [%s]' % (
                item.get('datetime').strftime('%Y-%m-%d %H:%M'),
                item.get('url'),
                item.get('title', '')
            )
            self.bot.privmsg(target, msg)
