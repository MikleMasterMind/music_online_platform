import gettext
import locale


LOCALES = {
    ("ru_RU", "UTF-8"): gettext.translation("window-domain",
                                            "l10n",
                                            ["ru_RU.UTF-8"],
                                            fallback=True),
    ("en_US", "UTF-8"): gettext.NullTranslations(),
}

def _(text: str) -> str:
    return LOCALES[locale.getlocale()].gettext(text)

locale.setlocale(locale.LC_ALL, ("ru_RU", "UTF-8"))
