# Email backend
EMAIL_BACKEND_DEV = 'django.core.mail.backends.console.EmailBackend'

ANYMAIL = {
    "MAILGUN_API_KEY": "2a982de42eedd4b4a923a1084a454cf0-af6c0cec-013d6cb9",
    "MAILGUN_SENDER_DOMAIN": 'sandboxa9413bd50595408390d634130398e610.mailgun.org'
}

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
DEFAULT_FROM_EMAIL = "vwapplication@gmail.com"