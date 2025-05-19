from storages.backends.s3boto3 import S3StaticStorage, S3Boto3Storage


class StaticStorage(S3StaticStorage):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False