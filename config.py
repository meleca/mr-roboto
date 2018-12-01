from os import path
from irc3 import utils
from decouple import config, Csv


class Config(utils.Config):
    """Configuration settings.

    All user defined configurations are loaded from
    local settings file and environment variables.
    """
    def __init__(self, *args, **kwargs):
        """Initializes configuration settings."""
        super(Config, self).__init__(*args, **kwargs)

        # Always load the default settings.
        file_name = 'settings.default.ini'
        file_path = path.dirname(path.abspath(__file__))
        full_path = path.join(file_path, file_name)
        base_conf = utils.parse_config('bot', full_path)
        self.update(**base_conf)

        # If there is an user defined settings file.
        user_path = path.join(file_path, file_name.replace('.default', ''))
        user_conf = (utils.parse_config('bot', user_path)
                     if path.isfile(user_path) else {})
        self.update(**user_conf)

        # Override settings using user defined environment variables.
        env_vars = {key: value for key, value in filter(
            lambda key_val: key_val[1], [
                ('host', config('IRC_HOST', default='')),
                ('port', config('IRC_PORT', default=0, cast=int)),
                ('nick', config('IRC_NICK', default='')),
                ('username', config('IRC_USERNAME', default='')),
                ('password', config('IRC_PASSWORD', default='')),
                ('autojoins', config('IRC_AUTOJOINS', default='', cast=Csv())),
                ('database', config('DATABASE_URL', default='')),
                ('ssl', config('IRC_SSL', default=False, cast=bool)),
                ('ssl_verify', config('IRC_SSL_VERIFY', default='')),
                ('sasl_username', config('IRC_SASL_USERNAME', default='')),
                ('sasl_password', config('IRC_SASL_PASSWORD', default=''))
            ]
        )}
        self.update(**env_vars)

        # For the admin list it is necessary
        # to convert nicknames into masks
        # and add one by one to a sub-dict.
        admins = config('IRC_ADMINS', default='', cast=Csv())
        admkey = 'irc3.plugins.command.masks'
        if admins:
            for admin in admins:
                self[admkey][f'{admin}!*@*'] = 'all_permissions'


conf = Config()
