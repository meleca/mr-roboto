from unittest import mock
from plugins.database import Database


@mock.patch('plugins.database.dataset')
def test_database_connection(mock_dataset, bot):
    """Tests the initialization of Database plugin.

    It creates a database connection using dataset library.

    Args:
        mock_dataset: Fakes dataset library.
        bot: Fake instance of an Irc3Bot.
    """
    con = mock.Mock()
    mock_dataset.connect.return_value = con
    Database(bot)
    assert mock_dataset.connect.called_once_with(bot.config.database)
    assert bot.dataset == con
