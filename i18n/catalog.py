# For new languages support add the desired lang codes here. The codes
# must follow the two-letter lower case abbreviation according to the
# ISO639-1 (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
# e.g.: fr (french), de (german), pt (portuguese), and so on.
languages = ['en']

# Add here the text that should be translated. An entry is a python
# dictionary and must have at least a `msgid` field with the text in
# english as it is the default language. The text translated goes just
# after the `msgid` and the key is the language code. The following
# example is an entry with a text in english, portuguese and spanish.
# e.g.:
#
# {
#     'msgid': 'Hello world',
#     'pt': 'Olá mundo',
#     'es': 'Hola mundo'
# }
entries = [
    {
        'msgid': 'Good morning'
    },
    {
        'msgid': 'Good morning fellas'
    },
    {
        'msgid': 'Morning'
    },
    {
        'msgid': 'Hello everyone'
    },
    {
        'msgid': 'I definitely need a coffee. Oh, hello btw.'
    },
    {
        'msgid': 'Lunch time'
    },
    {
        'msgid': 'I\'m gonna get something to eat'
    },
    {
        'msgid': '{nick}: Hi!'
    },
    {
        'msgid': 'Booom shakalaka'
    },
    {
        'msgid': 'It seems this site has a broken charset'
    },
    {
        'msgid': 'Looks like an image'
    },
    {
        'msgid': 'Do you know I\'m deaf right?'
    },
    {
        'msgid': 'For God sake I\'m blind'
    },
    {
        'msgid': 'What kind of weed is that?'
    },
    {
        'msgid': 'My sources say that this links does not exists'
    },
    {
        'msgid': 'I\'m sorry but the stars seems to be unreachable.'
    },
    {
        'msgid': 'Okie dokie'
    },
    {
        'msgid': 'Sorry, looks like something went wrong :('
    },
    {
        'msgid': 'All work and no play makes Jack a dull boy'
    },
    {
        'msgid': (
            'Hi there, my name is {nick} and I am an IRC bot '
            'written in Python. If you wanna know more about me take '
            'a look at my Github page https://github.com/meleca/mr-roboto/. '
            'Currently running v{version}.'
        )
    }
]
