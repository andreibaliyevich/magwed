from os.path import splitext
from django.utils import timezone


def get_article_path(instance, filename):
    """ Get path of article """
    filepath = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'articles/{filepath}{file_ext}'
