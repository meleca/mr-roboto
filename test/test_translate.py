import gettext
from i18n import catalog, translate
import os
import shutil


def test_translation():
    """Tests if the translation function returns a Translation
    instance.

    The translation object returned can be both a GNUTranslations or
    a NullTranslations depending if there's a locale directory with
    valid translations or not.
    """
    gt = translate.translation()
    assert isinstance(gt, gettext.NullTranslations)


def test_build():
    """Tests if the build function produces the appropriate
    localization files."""
    if os.path.isdir(translate.LOCALE_DIR):
        shutil.rmtree(translate.LOCALE_DIR)
    translate.build()
    for lang in catalog.languages:
        path = os.path.join(translate.LOCALE_DIR, lang, 'LC_MESSAGES')
        po_file = os.path.join(path, f'{translate.NAMESPACE}.po')
        mo_file = os.path.join(path, f'{translate.NAMESPACE}.mo')
        assert os.path.isfile(po_file)
        assert os.path.isfile(mo_file)
