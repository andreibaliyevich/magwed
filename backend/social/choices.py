from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class LinkType(TextChoices):
    FACEBOOK = 'facebook', _('Facebook')
    TWITTER = 'twitter', _('Twitter')
    INSTAGRAM = 'instagram', _('Instagram')
    LINKEDIN = 'linkedin', _('LinkedIn')
    SPOTIFY = 'spotify', _('Spotify')
    YOUTUBE = 'youtube', _('YouTube')
    SOUNDCLOUD = 'soundcloud', _('SoundCloud')
    PINTEREST = 'pinterest', _('Pinterest')
