__author__ = 'abdallah'

from dev import *
from django.conf.global_settings import LANGUAGES

if FEATURES['ENABLE_LANGUAGE_CHANGE']:
    USE_I18N = True
    TIME_ZONE = 'Asia/Amman'
    LANGUAGE_CODE = 'en-us'

    ugettext = lambda s: s
    LANGUAGES = (
        ('ar', ugettext('Arabic')),
        ('en', ugettext('English')),
    )
