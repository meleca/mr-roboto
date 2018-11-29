from irc3 import utils
from decouple import config, Csv


class Config(utils.Config):
    """Configuration settings.

    All user defined configurations are
    loaded from environment variables.
    """
    def __init__(self, *args, **kwargs):
        """Initializes configuration settings."""
        super(Config, self).__init__(*args, **kwargs)
        self.update(**{
            'host': config('HOST', default='localhost'),
            'port': config('PORT', default=6667, cast=int),
            'nick': config('NICK', default='mybot'),
            'username': config('USERNAME', default='mybot'),
            'autojoins': config('AUTOJOINS', default='', cast=Csv()),
            'database': config('DATABASE_URL', default='sqlite:///:memory:'),
            'includes': [
                'irc3.plugins.command',
                'irc3.plugins.log',
                'irc3.plugins.autojoins',
                'irc3.plugins.userlist',
                'plugins.database',
                'plugins.commands',
                'plugins.behaviors'
            ],
            'irc3.plugins.command': {
                'cmd': '!',
                'guard': 'irc3.plugins.command.mask_based_policy'
            },
            'irc3.plugins.command.masks': {
                '*': 'view'
            }
        })

        # Loads optional configurations.
        optional = {}

        ssl = config('SSL', default=False, cast=bool)
        if ssl:
            optional['ssl'] = ssl

        ssl_verify = config('SSL_VERIFY', default='')
        if ssl_verify:
            optional['ssl_verify'] = ssl_verify

        sasl_username = config('SASL_USERNAME', default='')
        if sasl_username:
            optional['sasl_username'] = sasl_username

        sasl_password = config('SASL_PASSWORD', default='')
        if sasl_password:
            optional['sasl_password'] = sasl_password

        self.update(**optional)

        # For the admin list it is necessary
        # to convert nicknames into masks
        # and add one by one to a sub-dict.
        admins = config('ADMINS', default='', cast=Csv())
        admkey = 'irc3.plugins.command.masks'
        if admins:
            for admin in admins:
                self[admkey][f'{admin}!*@*'] = 'all_permissions'


conf = Config()
