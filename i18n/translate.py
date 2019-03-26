import argparse
import datetime
import gettext
import os
import polib
from i18n import catalog

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOCALE_DIR = os.path.join(ROOT_DIR, 'locale')
NAMESPACE = 'mr_roboto'


def translation():
    """Return a translation instance according
    to the namespace and locale."""
    return gettext.translation(NAMESPACE, LOCALE_DIR, fallback=True)


# Set an alias for the translation method
_ = translation().gettext


def build():
    """Build translation catalogs."""
    metadata = {
        'POT-Creation-Date': datetime.datetime.now(),
        'PO-Revision-Date': datetime.datetime.now(),
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit'
    }
    for lang in catalog.languages:
        po = polib.POFile()
        po.metadata = metadata
        for entry in catalog.entries:
            po.append(
                polib.POEntry(
                    msgid=entry['msgid'],
                    msgstr=entry.get(lang, '')
                )
            )
        path = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES')
        if not os.path.isdir(path):
            os.makedirs(path)
        po.save(os.path.join(path, f'{NAMESPACE}.po'))
        po.save_as_mofile(os.path.join(path, f'{NAMESPACE}.mo'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Internationalization utils.')
    parser.add_argument(
        '-b', '--build',
        action='store_true',
        help='build translation catalogs'
    )
    args = parser.parse_args()
    if args.build:
        build()
