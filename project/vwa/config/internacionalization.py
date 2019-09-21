# Internationalization

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
PORTUGUESE = 'pt-BR'
ENGLISH = 'en-us'
LANGUAGE_CODE = PORTUGUESE

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
INTERNATIONALIZATION = True
USE_I18N = INTERNATIONALIZATION

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
FORMAT_DATES = True
USE_L10N = FORMAT_DATES

# If you set this to False, Django will not use timezone-aware datetimes.
TIMEZONE_DATETIMES = True
USE_TZ = TIMEZONE_DATETIMES