from decouple import config


if config('DEBUG', default=True, cast=bool) is False:
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_LOCATION = "media"
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'