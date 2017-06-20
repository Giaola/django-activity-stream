from django.core.exceptions import ImproperlyConfigured

from actstream import settings
from actstream.signals import action
from actstream.compat_apps import AppConfig


class ActstreamConfig(AppConfig):
    name = 'actstream'

    def ready(self):
        from actstream.actions import action_handler
        action.connect(action_handler, dispatch_uid='actstream.models')
        action_class = self.get_model('action')

        if settings.USE_JSONFIELD:
            try:
                from django.contrib.postgres.fields import JSONField
                JSONField(blank=True, null=True).contribute_to_class(action_class, 'data')
            except ImportError:
                raise ImproperlyConfigured('Django version(>=1.11) that supports postgres JSONField is required.')

