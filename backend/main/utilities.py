from os.path import splitext
from django.conf import settings
from django.utils import timezone, translation


def get_translated_field(instance, field_name):
    """ Get Translated Field """
    lang_code = translation.get_language()
    if lang_code == settings.LANGUAGE_CODE:
        return getattr(instance, field_name)
    else:
        translations = instance.translations.filter(
            language=lang_code,
        ).first() or instance
        return getattr(translations, field_name)


def get_cover_path(instance, filename):
    """ Get path of cover """
    filepath = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'covers/{filepath}{file_ext}'


def get_thumbnail_path(instance, filename):
    """ Get path of thumbnail """
    filepath = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'thumbnails/{filepath}{file_ext}'


def get_magazine_path(instance, filename):
    """ Get path of Magazine """
    filepath = timezone.now().strftime('%Y/%m-%d-%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'magazines/{filepath}{file_ext}'
