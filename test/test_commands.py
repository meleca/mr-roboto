import asyncio
import asynctest
from pytest import mark
from irc3.utils import IrcString
from plugins.commands import Commands


def test_commands_initialization(bot):
    """Tests the initialization of Commands plugin.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    plugin = Commands(bot)
    assert isinstance(plugin, Commands)
    assert plugin.bot == bot


@asynctest.patch('plugins.commands.aiohttp.ClientSession.get')
def test_commit(mock_session_get, bot):
    """Tests the commit command.

    Args:
        mock_session_get: Fakes aiohttp.ClientSession.get method.
        bot: Fake instance of an Irc3Bot.
    """
    data = 'Can someone review this commit, please?'
    request = asynctest.Mock(text=asynctest.CoroutineMock(side_effect=[data]))
    mock_session_get.return_value.__aenter__.return_value = request
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    plugin = Commands(bot)

    async def test():
        response = await plugin.commit(mask, channel, None)
        assert response == data
    asyncio.get_event_loop().run_until_complete(test())


@asynctest.patch('plugins.commands.aiohttp.ClientSession.get')
def test_excuse(mock_session_get, bot):
    """Tests the excuse command.

    Args:
        mock_session_get: Fakes aiohttp.ClientSession.get method.
        bot: Fake instance of an Irc3Bot.
    """
    data = 'The user must not know how to use it'
    request = asynctest.Mock(text=asynctest.CoroutineMock(side_effect=[data]))
    mock_session_get.return_value.__aenter__.return_value = request
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    plugin = Commands(bot)

    async def test():
        response = await plugin.excuse(mask, channel, None)
        assert response == data
    asyncio.get_event_loop().run_until_complete(test())


@mark.parametrize('sign,expected', [
    ('Sagittarius', '... Be hopeful.'),
    ('Foobar', 'Foobar is not a valid sign.')
])
@asynctest.patch('plugins.commands.aiohttp.ClientSession.get')
def test_horoscope(mock_session_get, sign, expected, bot):
    """Tests the horoscope command.

    Args:
        mock_session_get: Fakes aiohttp.ClientSession.get method.
        sign: A zodiac sign.
        expected: The expected response.
        bot: Fake instance of an Irc3Bot.
    """
    data = {'horoscope': expected}
    request = asynctest.Mock(json=asynctest.CoroutineMock(side_effect=[data]))
    mock_session_get.return_value.__aenter__.return_value = request
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    args = {'<sign>': sign}
    plugin = Commands(bot)

    async def test():
        response = await plugin.horoscope(mask, channel, args)
        assert response == expected
    asyncio.get_event_loop().run_until_complete(test())


def test_greeting(bot):
    """Tests the greeting command.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    args = {
        '<nick>': 'nickname',
        '<message>': 'Hello there.'
    }
    data = {
        'channel': channel.replace('#', ''),
        'nick': args.get('<nick>'),
        'options': '\n'.join(['Hey there!', 'Hello there.'])
    }
    rule = ['channel', 'nick']
    plugin = Commands(bot)

    async def test():
        response = await plugin.greeting(mask, channel, args)
        assert bot.dataset['greetings'].upsert.called_once_with(data, rule)
        assert response == 'Okie dokie'
    asyncio.get_event_loop().run_until_complete(test())


def test_greeting_raising_exception(bot):
    """Tests the greeting command when error occur.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    bot.dataset['greetings'].upsert.side_effect = ValueError()
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    args = {
        '<nick>': 'nickname',
        '<message>': 'Hello there.'
    }
    plugin = Commands(bot)

    async def test():
        response = await plugin.greeting(mask, channel, args)
        assert response == 'Sorry, looks like something went wrong :('
    asyncio.get_event_loop().run_until_complete(test())


@mark.parametrize('subject,joke,expected', [
    ('', '', 'All work and no play makes Jack a dull boy'),
    (
        ['chuck', 'norris'],
        {'value': {'joke': 'Time waits for no man, except Chuck Norris.'}},
        'Time waits for no man, except Chuck Norris.'
    ),
    (
        ['yo', 'momma'],
        {'joke': 'Yo mama is so fat she can be my bear.'},
        'Yo mama is so fat she can be my bear.'
    )
])
@asynctest.patch('plugins.commands.aiohttp.ClientSession.get')
def test_joke(mock_session_get, subject, joke, expected, bot):
    """Tests the joke command.

    Args:
        mock_session_get: Fakes aiohttp.ClientSession.get method.
        subject: A joke subject.
        joke: Fake joke service response.
        expected: The expected response.
        bot: Fake instance of an Irc3Bot.
    """
    request = asynctest.Mock(json=asynctest.CoroutineMock(side_effect=[joke]))
    mock_session_get.return_value.__aenter__.return_value = request
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    args = {'<subject>': subject}
    plugin = Commands(bot)

    async def test():
        response = await plugin.joke(mask, channel, args)
        assert response == expected
    asyncio.get_event_loop().run_until_complete(test())


def test_cebolate(bot):
    """Tests the cebolate command.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    args = {'<message>': ['CORRECT', 'answer']}
    plugin = Commands(bot)

    async def test():
        response = await plugin.cebolate(mask, channel, args)
        assert response == 'COLLECT answel'
    asyncio.get_event_loop().run_until_complete(test())


@mark.parametrize('expected', [
    '2018-12-06 https://github.com/meleca/mr-roboto [mr-roboto]'
])
@mark.parametrize('keyword', ['mr-roboto', None])
@mark.parametrize('date', [
    'today', 'yesterday', 'week', 'month',
    'any', '2018-12-06', '2018-02-31'
])
@asynctest.patch('plugins.commands.or_')
def test_urls(mock_or_, date, keyword, expected, bot):
    """Tests the urls command.

    Args:
        mock_or_: Fakes sqlalchemy.sql.or_ function.
        date: An ISO date or special keyword.
        keyword: A list of keywords to be used for filtering.
        expected: Expected response.
        bot: Fake instance of an Irc3Bot.
    """
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    args = {'<date>': date, '<keyword>': keyword}
    expected = 'Invalid date' if date == '2018-02-31' else expected
    plugin = Commands(bot)
    asyncio.get_event_loop().run_until_complete(
        plugin.urls(mask, channel, args))
    assert bot.privmsg.called_once_with(channel, expected)


def test_slackers(bot):
    """Tests slackers command.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    args = {}
    expected = 'somebody_else (100), somebody (10)'
    plugin = Commands(bot)
    asyncio.get_event_loop().run_until_complete(
        plugin.slackers(mask, channel, args))
    assert bot.privmsg.called_once_with(channel, expected)


def test_karma(bot):
    """Tests karma command.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    args = {}
    expected = 'python (5), java (-10)'
    plugin = Commands(bot)
    asyncio.get_event_loop().run_until_complete(
        plugin.karma(mask, channel, args))
    assert bot.privmsg.called_once_with(channel, expected)
