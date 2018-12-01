from unittest import mock
from plugins.baseplugin import BasePlugin


def test_BasePlugin_reload():
    """Tests BasePlugin reload method."""
    bot = mock.Mock()
    old = BasePlugin(bot)
    new = BasePlugin.reload(old)
    assert isinstance(new, BasePlugin)
    assert new.bot == old.bot
