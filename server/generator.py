import hashlib
import shortuuid
from django.conf import settings
from django.utils.timezone import now


def short_token():
    # Hash as a application identifier or code
    cod = shortuuid.uuid().encode('utf-8')
    hash = hashlib.sha1(cod)
    hash.update(settings.SECRET_KEY.encode('utf-8'))
    return hash.hexdigest()[::2]


def long_token():
    # Hash as a application secret or token
    cod = shortuuid.uuid().encode('utf-8')
    hash = hashlib.sha1(cod)
    hash.update(settings.SECRET_KEY.encode('utf-8'))
    return hash.hexdigest()


def get_token_expiry(public=True):
    if public:
        return now() + settings.EXPIRE_DELTA_PUBLIC
    else:
        return now() + settings.EXPIRE_DELTA


def get_code_expiry():
    return now() + settings.EXPIRE_CODE_DELTA
