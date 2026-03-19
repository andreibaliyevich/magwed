from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MessengerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messenger'
    verbose_name = _('Messenger')

    def ready(self):
        from django.core.cache import caches

        caches['connections'].clear()
