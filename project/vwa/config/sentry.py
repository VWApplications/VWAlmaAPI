from sentry_sdk.integrations.django import DjangoIntegration
import sentry_sdk


sentry_sdk.init(
    dsn="https://8df5acb722db4dd1bd0c257dcb10e981@sentry.io/1757237",
    integrations=[DjangoIntegration()]
)