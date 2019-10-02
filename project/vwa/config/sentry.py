from sentry_sdk.integrations.django import DjangoIntegration
from decouple import config
import sentry_sdk


sentry_sdk.init(
    dsn=config('SENTRY'),
    integrations=[DjangoIntegration()]
)