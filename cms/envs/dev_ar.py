__author__ = 'abdallah'

from .dev import *

USE_I18N = True
TIME_ZONE = 'America/Guayaquil'
LANGUAGE_CODE = 'en'

ugettext = lambda s: s
LANGUAGES = (
    ('ar', ugettext('Arabic')),
    ('en', ugettext('English')),
)
