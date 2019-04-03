# For new languages support add the desired lang codes here. The codes
# must follow the two-letter lower case abbreviation according to the
# ISO639-1 (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
# e.g.: fr (french), de (german), pt (portuguese), and so on.
languages = ['en', 'pt']

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
        'msgid': 'Good morning',
        'pt': 'Bom dia'
    },
    {
        'msgid': 'Good morning fellas',
        'pt': 'Bom dia pessoal'
    },
    {
        'msgid': 'Morning',
        'pt': 'Dia'
    },
    {
        'msgid': 'Hello everyone',
        'pt': 'Olá para todos'
    },
    {
        'msgid': 'I definitely need a coffee. Oh, hello btw.',
        'pt': (
            'Eu definitivamente preciso de um café. '
            'Oh, antes que eu me esqueça, olá.'
        )
    },
    {
        'msgid': 'Lunch time',
        'pt': 'Hora do almoço'
    },
    {
        'msgid': 'I\'m gonna get something to eat',
        'pt': 'Eu vou pegar algo para comer'
    },
    {
        'msgid': '{nick}: Hi!',
        'pt': '{nick}: Oi!'
    },
    {
        'msgid': 'Booom shakalaka'
    },
    {
        'msgid': 'It seems this site has a broken charset',
        'pt': 'Esse site parece ter um charset inválido'
    },
    {
        'msgid': 'Looks like an image',
        'pt': 'Parece uma imagem'
    },
    {
        'msgid': 'Do you know I\'m deaf right?',
        'pt': 'Você sabe que eu sou surdo?'
    },
    {
        'msgid': 'For God sake I\'m blind',
        'pt': 'Por Deus, eu sou cego!'
    },
    {
        'msgid': 'What kind of weed is that?',
        'pt': 'Que matinho é esse?'
    },
    {
        'msgid': 'My sources say that this links does not exists',
        'pt': 'Minhas fontes me dizem que esse link não existe'
    },
    {
        'msgid': 'I\'m sorry but the stars seems to be unreachable.',
        'pt': 'Sinto muito mas os astros parecem estar inacessíveis.'
    },
    {
        'msgid': 'Okie dokie',
        'pt': 'Já é'
    },
    {
        'msgid': 'Sorry, looks like something went wrong :(',
        'pt': 'Sinto muito mas parece que algo deu errado :('
    },
    {
        'msgid': 'All work and no play makes Jack a dull boy',
        'pt': 'Só trabalho, sem diversão, fazem de Jack um bobão'
    },
    {
        'msgid': (
            'Hi there, my name is {nick} and I am an IRC bot '
            'written in Python. If you wanna know more about me take '
            'a look at my Github page https://github.com/meleca/mr-roboto/. '
            'Currently running v{version}.'
        ),
        'pt': (
            'Olá, meu nome é {nick} e eu sou um bot para IRC escrito '
            'em Python. Se você quer saber mais sobre mim, de uma '
            'olhada na minha página no Github '
            'https://github.com/meleca/mr-roboto/. '
            'Atualmente rodando a versão {version}.'
        )
    }
]
