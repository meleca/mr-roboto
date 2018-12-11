import asyncio
import asynctest
from pytest import mark
from unittest import mock
from irc3.utils import IrcString
from plugins.behaviors import Behaviors


def test_behaviors_initialization(bot):
    """Tests the initialization of Behaviors plugin.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    plugin = Behaviors(bot)
    assert isinstance(plugin, Behaviors)
    assert plugin.bot == bot


def test_behaviors_compile_rules_none(bot):
    """Tests _compile_rules method being called with an empty param.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    plugin = Behaviors(bot)
    rules = plugin._compile_rules(None)
    assert not rules


def test_behaviors_good_morning(bot):
    """Tests good_morning method by simply calling it.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    plugin = Behaviors(bot)
    plugin.good_morning()
    assert bot.privmsg.called_once


def test_behaviors_lunch_time(bot):
    """Tests lunch_time method by simply calling it.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    plugin = Behaviors(bot)
    plugin.lunch_time()
    assert bot.privmsg.called_once


def test_behaviors_say_hi(bot):
    """Tests say_hi method by simply calling it.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    plugin = Behaviors(bot)
    plugin.say_hi(mask, channel)
    assert bot.privmsg.called_once_with(channel, 'mybot: Hey there!')


@asynctest.patch.object(Behaviors, 'karma')
@asynctest.patch.object(Behaviors, 'slack_meter')
@asynctest.patch.object(Behaviors, 'handle_url')
def test_behaviors_handle_message(
    mock_handle_url, mock_slack_meter, mock_karma, bot
):
    """Tests handle_message method simulating an URL read from channel.

    Args:
        mock_handle_url: Fakes Behaviors.handle_url method.
        mock_slack_meter: Fakes Behaviors.slack_meter method.
        bot: Fake instance of an Irc3Bot.
    """
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    data = 'https://github.com/meleca/mr-roboto'
    plugin = Behaviors(bot)
    asyncio.get_event_loop().run_until_complete(
        plugin.handle_message(mask=mask, target=channel, data=data))
    assert mock_handle_url.called_once_with(channel, data.encode('utf-8'))
    assert mock_slack_meter.called_once_with(
        channel=channel, nick=mask.nick, message=data)
    assert not mock_karma.called


@asynctest.patch.object(Behaviors, 'handle_url')
def test_behaviors_handle_message_raising_exception(mock_handle_url, bot):
    """Tests handle_message method simulating an
    URL read from channel and raising an exception.

    Args:
        mock_handle_url: Fakes Behaviors.handle_url method.
        bot: Fake instance of an Irc3Bot.
    """
    mask = IrcString('nickname!@192.168.0.100')
    channel = IrcString('#meleca')
    data = 'https://github.com/meleca/mr-roboto'
    mock_handle_url.side_effect = ValueError()
    plugin = Behaviors(bot)
    asyncio.get_event_loop().run_until_complete(
        plugin.handle_message(mask=mask, target=channel, data=data))
    assert bot.privmsg.called_once_with(channel, 'Booom shakalaka')


@mark.parametrize('header,data,message', [
    ('text/html', b'<head><title>The title</title></head>', '[The title]'),
    ('image/png', None, 'Looks like an image'),
    ('audio/ogg', None, 'Do you know I\'m deaf right?'),
    ('video/mp4', None, 'For God sake I\'m blind'),
    ('application/pdf', None, 'What kind of weed is that?'),
    ('', None, 'My sources say that this links does not exists'),
    ('text/html', '<h1>âçàí'.encode('latin-1'), ''),
    ('text/html', 'âçàí'.encode('latin-1'),
     'It seems this site has a broken charset')
])
@asynctest.patch('plugins.behaviors.aiohttp.ClientSession.get')
def test_behaviors_handle_url(mock_session_get, header, data, message, bot):
    """Tests handle_url method simulating all
    expected types of valid and invalid entries.

    Args:
        mock_session_get: Fakes aiohttp.ClientSession.get method.
        header: An fake HTTP request response header.
        data: An fake HTTP request response content.
        message: The expected bot's response.
        bot: Fake instance of an Irc3Bot.
    """
    channel = IrcString('#meleca')
    url = b'https://github.com/meleca/mr-roboto'
    request = mock.Mock(
        headers={'CONTENT-TYPE': header},
        charset='utf-8',
        read=asynctest.CoroutineMock(side_effect=[data])
    )
    mock_session_get.return_value.__aenter__.return_value = request
    plugin = Behaviors(bot)
    asyncio.get_event_loop().run_until_complete(
        plugin.handle_url(channel, url))
    assert bot.privmsg.called_once_with(channel, message)
    assert bot.dataset['url_history'].upsert.called_once


def test_behaviors_slack_meter(bot):
    """Tests slack_meter method.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    channel = IrcString('#meleca')
    nick = 'somebody'
    msg = 'Do you think I talk too much?'
    plugin = Behaviors(bot)
    asyncio.get_event_loop().run_until_complete(
        plugin.slack_meter(channel, nick, msg))
    assert bot.dataset['slackers'].upsert.called_once


def test_behaviors_karma(bot):
    """Tests karma method.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    channel = IrcString('#meleca')
    entity = b'python++'
    plugin = Behaviors(bot)
    asyncio.get_event_loop().run_until_complete(
        plugin.karma(channel, entity))
    assert bot.dataset['karma'].upsert.called_once
    assert bot.privmsg.called_once_with(channel, 'python (6)')
