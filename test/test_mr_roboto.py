import mr_roboto
from os import path
from unittest import mock
from pytest import mark


@mock.patch('mr_roboto.ReloadEventHandler')
@mock.patch('mr_roboto.Observer')
@mock.patch('mr_roboto.IrcBot')
def test_main(mock_ircbot, mock_observer, mock_reloader, root_directory, bot):
    """Tests bot regular initialization.

    Args:
        mock_ircbot: Fakes IrcBot from irc3 library.
        mock_observer: Fakes the Observer from watchdog library.
        mock_reloader: Fakes the ReloadEventHandler class.
        root_directory: Path to the application's root directory.
        bot: Fake instance of an Irc3Bot.
    """
    observer = mock.Mock()
    reloader = mock.Mock()
    mock_ircbot.from_config.return_value = bot
    mock_observer.return_value = observer
    mock_reloader.return_value = reloader
    mr_roboto.main()
    assert mock_ircbot.from_config.called_once_with(mr_roboto.conf)
    assert mock_reloader.called_once_with(bot, mr_roboto.conf)
    assert mock_observer.called_once
    assert observer.schedule.called_once_with(
        reloader, root_directory, recursive=True)
    assert observer.start.called_once
    assert bot.run.called_once_with(forever=True)


@mark.parametrize('version,expected', [
    ('0.1.0', '0.1.0'),
    ('0.1.a', '?.?.?'),
    ('xx.1.0', '?.?.?'),
])
def test_get_version_from_file(version, expected):
    """Tests the error path for get_version_from_file().

    Args:
        version: A fake version number that will be used with a fake file.
        expected: The expected version returned from the tested function.
    """
    mock_file = mock.mock_open(read_data=f'VERSION = {version}')
    with mock.patch('mr_roboto.open', mock_file) as f:
        assert mr_roboto.get_version_from_file(f) == expected

    assert mr_roboto.get_version_from_file('') == '?.?.?'


@mock.patch('mr_roboto.ReloadEventHandler')
@mock.patch('mr_roboto.Observer')
@mock.patch('mr_roboto.IrcBot')
def test_main_kbinterrupt(
    mock_ircbot, mock_observer, mock_reloader, root_directory, bot
):
    """Tests keyboard interruption after bot's initialization.

    Args:
        mock_ircbot: Fakes IrcBot from irc3 library.
        mock_observer: Fakes the Observer from watchdog library.
        mock_reloader: Fakes the ReloadEventHandler class.
        root_directory: Path to the application's root directory.
        bot: Fake instance of an Irc3Bot.
    """
    bot.run.side_effect = KeyboardInterrupt()
    observer = mock.Mock()
    reloader = mock.Mock()
    mock_ircbot.from_config.return_value = bot
    mock_observer.return_value = observer
    mock_reloader.return_value = reloader
    mr_roboto.main()
    assert mock_ircbot.from_config.called_once_with(mr_roboto.conf)
    assert mock_reloader.called_once_with(bot, mr_roboto.conf)
    assert mock_observer.called_once
    assert observer.schedule.called_once_with(
        reloader, root_directory, recursive=True)
    assert observer.start.called_once
    assert bot.run.called_once_with(forever=True)
    assert observer.stop.called_once


def test_ReloadEventHandler_on_modified(root_directory, bot):
    """Tests the app reload handler for source code changes.

    Args:
        root_directory: Path to the application's root directory.
        bot: Fake instance of an Irc3Bot.
    """
    event = mock.Mock()
    event.src_path = path.join(root_directory, 'plugins', 'behaviors.py')
    reloader = mr_roboto.ReloadEventHandler(bot, mr_roboto.conf)
    reloader.on_modified(event)
    assert bot.reload.called_once


def test_ReloadEventHandler_on_modified_untracked(root_directory, bot):
    """Tests the app reload handler when the changed
    file is not on the tracking list.

    Args:
        root_directory: Path to the application's root directory.
        bot: Fake instance of an Irc3Bot.
    """
    event = mock.Mock()
    event.src_path = path.join(root_directory, 'alembic.ini')
    reloader = mr_roboto.ReloadEventHandler(bot, mr_roboto.conf)
    reloader.on_modified(event)
    assert not bot.reload.called
