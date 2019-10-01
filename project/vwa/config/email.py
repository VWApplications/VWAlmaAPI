# Email backend
EMAIL_BACKEND_DEV = 'django.core.mail.backends.console.EmailBackend'

ANYMAIL = {
    "MAILGUN_API_KEY": "7d960b116ec69cb3bd909ba25706041a-f877bd7a-351943a5",
    "MAILGUN_SENDER_DOMAIN": 'sandbox43d3bc2d2ec44a6688b52d324f1f7cb3.mailgun.org'
}

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
DEFAULT_FROM_EMAIL = "victorhad@gmail.com"