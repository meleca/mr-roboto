from i18n import catalog


def test_languages():
    """Tests if all languages code follows the pattern."""
    assert all(
        len(lang) == 2 and lang.islower()
        for lang in catalog.languages
    )


def test_entries():
    """Tests if all entries have a valid msgid."""
    assert all(
        'msgid' in entry.keys() and entry['msgid']
        for entry in catalog.entries
    )
