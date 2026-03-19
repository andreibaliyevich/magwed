from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = _('Accounts')

    def ready(self):
        from django.db import connection
        from .models import ConnectionHistory

        table_names = connection.introspection.table_names()

        if 'accounts_connectionhistory' in table_names:
            ConnectionHistory.objects.update(online=False)
