# Third Party Library Imports
from django.conf import settings
from hashids import Hashids

hashid = Hashids(
    min_length=8,
    salt=getattr(settings, 'HASHIDS_SALT', ''),
    alphabet='0123456789ACDEFGHIJKLOQRSTUVWXYZ',
)

def encode(num):
    return hashid.encode(num)
