from django.apps import AppConfig


class FitbuddyConfig(AppConfig):
    name = 'fitbuddy'

    def ready(self):
        from . import signals