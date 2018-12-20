import pytest
from os import path
from unittest import mock
from datetime import datetime


@pytest.fixture
def root_directory():
    """App root directory."""
    return path.dirname(path.abspath(__file__))


@pytest.fixture
def bot():
    """Fake instance of an Irc3Bot."""
    mock_bot = mock.Mock()
    mock_bot.nick = 'mybot'
    mock_bot.version = '0.1.0'
    mock_bot.config = mock.Mock(database='sqlite:///:memory:')
    mock_bot.channels = ['#meleca']

    # A few database mock workarounds.
    class MockDatetime(datetime):
        def __neg__(self):
            return self
    tb_greetings = mock.Mock()
    tb_greetings.find_one.return_value = {'options': 'Hey there!'}
    tb_url_history = mock.Mock()
    tb_url_history.table.c.datetime = MockDatetime.utcnow()
    tb_slackers = mock.Mock()
    tb_slackers.find_one.return_value = {'words': 100}
    tb_slackers.find.return_value = [
        {'nick': 'somebody', 'words': 10},
        {'nick': 'somebody_else', 'words': 100}
    ]
    tb_karma = mock.Mock()
    tb_karma.find_one.return_value = {'status': 5}
    tb_karma.find.return_value = [
        {'entity': 'python', 'status': 5},
        {'entity': 'java', 'status': -10}
    ]
    database = {
        'greetings': tb_greetings,
        'karma': tb_karma,
        'slackers': tb_slackers,
        'url_history': tb_url_history
    }
    mock_bot.dataset = mock.MagicMock()
    mock_bot.dataset.query.return_value = [{
        'title': 'mr-roboto',
        'url': 'https://github.com/meleca/mr-roboto',
        'datetime': datetime.fromisoformat('2018-12-06')
    }]
    mock_bot.dataset.__contains__.side_effect = database.__contains__
    mock_bot.dataset.__getitem__.side_effect = database.__getitem__
    mock_bot.dataset.__iter__.side_effect = database.__iter__

    return mock_bot
