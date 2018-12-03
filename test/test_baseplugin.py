from plugins.baseplugin import BasePlugin


def test_BasePlugin_reload(bot):
    """Tests BasePlugin reload method.

    Args:
        bot: Fake instance of an Irc3Bot.
    """
    old = BasePlugin(bot)
    new = BasePlugin.reload(old)
    assert isinstance(new, BasePlugin)
    assert new.bot == old.bot
