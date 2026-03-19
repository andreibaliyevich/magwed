from os.path import splitext
from django.utils import timezone


def get_photo_path(instance, filename):
    """ Get path of photo """
    filepath = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'photos/{filepath}{file_ext}'
