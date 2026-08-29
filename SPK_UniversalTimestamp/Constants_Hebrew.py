"""
Constants_Hebrew — Hebrew-calendar month names, abbreviations, and
nominal lengths keyed by ISO language code.

**Purpose.**  Source of truth for `%B` / `%b` / `%m` formatting in
`Moment_cPresent_Hebrew.Present_Hebrew._strftime_month_attr`.
Marheshvan and Kislev carry inline ``# or 29`` / ``# or 30``
comments because their actual length varies by year (deficient /
regular / abundant); the calendrical code in `CC08_Hebrew` computes
the correct value at runtime.

**Public surface (star-exported via `__init__.py`).**
    `hebrew_MONTH_ATTS` (dict keyed `[language][months.MEMBER.value]
    -> {'name', 'abbrv', 'days'}`).

**Languages covered.**  ``'en'``, ``'fr'``, ``'es'``, ``'de'``, ``'it'``.

**Not in scope.**  Leap-year Adar handling (delegated to
`CC08_Hebrew`).  The two Adar entries here (ADAR_I, ADAR_II) are
only meaningful in leap years — in common years only ADAR is used
and the presentation layer maps to it explicitly.

**Change history.**  See `CHANGELOG.md`.
"""

from .CC08_Hebrew import months

# CONSTANTS #########################################################################################
hebrew_MONTH_ATTS = {
    'en': {
        months.NISAN.value: {'name': "Nisan", 'abbrv': "Nis", 'days': 30},
        months.IYYAR.value: {'name': "Iyyar", 'abbrv': "Iyy", 'days': 29},
        months.SIVAN.value: {'name': "Sivan", 'abbrv': "Siv", 'days': 30},
        months.TAMMUZ.value: {'name': "Tammuz", 'abbrv': "Tam", 'days': 29},
        months.AV.value: {'name': "Av", 'abbrv': "Av", 'days': 30},
        months.ELUL.value: {'name': "Elul", 'abbrv': "Elu", 'days': 29},
        months.TISHRI.value: {'name': "Tishri", 'abbrv': "Tis", 'days': 30},
        months.MARHESHVAN.value: {'name': "Marheshvan", 'abbrv': "Mar", 'days': 29},  # or 30
        months.KISLEV.value: {'name': "Kislev", 'abbrv': "Kis", 'days': 30},  # or 29
        months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
        months.SHEVAT.value: {'name': "Shevat", 'abbrv': "She", 'days': 30},
        months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
        months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
    },
    'fr': {
        months.NISAN.value: {'name': "Nissan", 'abbrv': "Nis", 'days': 30},
        months.IYYAR.value: {'name': "Iyar", 'abbrv': "Iyy", 'days': 29},
        months.SIVAN.value: {'name': "Sivan", 'abbrv': "Siv", 'days': 30},
        months.TAMMUZ.value: {'name': "Tammouz", 'abbrv': "Tam", 'days': 29},
        months.AV.value: {'name': "Av", 'abbrv': "Av", 'days': 30},
        months.ELUL.value: {'name': "Eloul", 'abbrv': "Elu", 'days': 29},
        months.TISHRI.value: {'name': "Tichri", 'abbrv': "Tis", 'days': 30},
        months.MARHESHVAN.value: {'name': "Marheshvan", 'abbrv': "Mar", 'days': 29},  # or 30
        months.KISLEV.value: {'name': "Kislev", 'abbrv': "Kis", 'days': 30},  # or 29
        months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
        months.SHEVAT.value: {'name': "Shevat", 'abbrv': "She", 'days': 30},
        months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
        months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
    },
    'es': {
        months.NISAN.value: {'name': "Nisán", 'abbrv': "Nis", 'days': 30},
        months.IYYAR.value: {'name': "Iyar", 'abbrv': "Iyy", 'days': 29},
        months.SIVAN.value: {'name': "Siván", 'abbrv': "Siv", 'days': 30},
        months.TAMMUZ.value: {'name': "Tamuz", 'abbrv': "Tam", 'days': 29},
        months.AV.value: {'name': "Av", 'abbrv': "Av", 'days': 30},
        months.ELUL.value: {'name': "Elul", 'abbrv': "Elu", 'days': 29},
        months.TISHRI.value: {'name': "Tishri", 'abbrv': "Tis", 'days': 30},
        months.MARHESHVAN.value: {'name': "Marheshván", 'abbrv': "Mar", 'days': 29},  # or 30
        months.KISLEV.value: {'name': "Kislev", 'abbrv': "Kis", 'days': 30},  # or 29
        months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
        months.SHEVAT.value: {'name': "Shevat", 'abbrv': "She", 'days': 30},
        months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
        months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
    },
    'de': {
        months.NISAN.value: {'name': "Nisan", 'abbrv': "Nis", 'days': 30},
        months.IYYAR.value: {'name': "Ijar", 'abbrv': "Iyy", 'days': 29},
        months.SIVAN.value: {'name': "Siwan", 'abbrv': "Siv", 'days': 30},
        months.TAMMUZ.value: {'name': "Tammus", 'abbrv': "Tam", 'days': 29},
        months.AV.value: {'name': "Aw", 'abbrv': "Av", 'days': 30},
        months.ELUL.value: {'name': "Elul", 'abbrv': "Elu", 'days': 29},
        months.TISHRI.value: {'name': "Tischri", 'abbrv': "Tis", 'days': 30},
        months.MARHESHVAN.value: {'name': "Marheschwan", 'abbrv': "Mar", 'days': 29},  # or 30
        months.KISLEV.value: {'name': "Kislew", 'abbrv': "Kis", 'days': 30},  # or 29
        months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
        months.SHEVAT.value: {'name': "Schewat", 'abbrv': "She", 'days': 30},
        months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
        months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
    },
    'it': {
        months.NISAN.value: {'name': "Nisàn", 'abbrv': "Nis", 'days': 30},
        months.IYYAR.value: {'name': "Iyar", 'abbrv': "Iyy", 'days': 29},
        months.SIVAN.value: {'name': "Sivàn", 'abbrv': "Siv", 'days': 30},
        months.TAMMUZ.value: {'name': "Tamuz", 'abbrv': "Tam", 'days': 29},
        months.AV.value: {'name': "Av", 'abbrv': "Av", 'days': 30},
        months.ELUL.value: {'name': "Elul", 'abbrv': "Elu", 'days': 29},
        months.TISHRI.value: {'name': "Tishrì", 'abbrv': "Tis", 'days': 30},
        months.MARHESHVAN.value: {'name': "Marhesvan", 'abbrv': "Mar", 'days': 29},  # or 30
        months.KISLEV.value: {'name': "Kislev", 'abbrv': "Kis", 'days': 30},  # or 29
        months.TEVET.value: {'name': "Tevet", 'abbrv': "Tev", 'days': 29},
        months.SHEVAT.value: {'name': "Shevat", 'abbrv': "She", 'days': 30},
        months.ADAR_I.value: {'name': "Adar I", 'abbrv': "Ad1", 'days': 30},  # in leap years
        months.ADAR_II.value: {'name': "Adar II", 'abbrv': "Ad2", 'days': 29}   # in leap years
    }
}

