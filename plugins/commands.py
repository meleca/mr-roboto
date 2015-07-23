# -*- coding: utf-8 -*-
"""
    Bot commands
"""
from irc3 import plugin
from irc3.plugins.command import command
import asyncio
import aiohttp
import re


@plugin
class Commands(object):
    """
    Handle commands called by users
    """

    def __init__(self, bot):
        self.bot = bot

    @command(permission='view')
    @asyncio.coroutine
    def horoscope(self, mask, target, args):
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
        request = yield from aiohttp.request('GET', 'http://developers.agenciaideias.com.br/horoscopo/json')
        response = yield from request.json()
        if (response and 'signos' in response):
            the_one = None
            for zodiac_name, zodiac_regex in zodiac_table.iteritems():
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
