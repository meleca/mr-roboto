from os import environ
from config import Config


def test_config_initialization():
    """Tests the config initialization."""
    cur_env = environ.copy()
    environ['IRC_ADMINS'] = 'somebody'
    config = Config()
    environ.clear()
    environ.update(cur_env)
    expected = [
        'host',
        'port',
        'nick',
        'username',
        'autojoins',
        'includes',
        'database',
        'irc3.plugins.command',
        'irc3.plugins.command.masks'
    ]
    assert all(key in config for key in expected)
