import pytest
from os import path
from unittest import mock


@pytest.fixture
def root_directory():
    """App root directory."""
    return path.dirname(path.abspath(__file__))


@pytest.fixture
def bot():
    """Fake instance of an Irc3Bot."""
    mock_bot = mock.Mock()
    mock_bot.nick = 'mybot'
    mock_bot.config = mock.Mock(database='sqlite:///:memory:')
    mock_bot.channels = ['#meleca']
    tb_greetings = mock.Mock()
    tb_greetings.find_one.return_value = {'options': 'Hey there!'}
    database = {'greetings': tb_greetings}
    mock_bot.dataset = database
    return mock_bot
