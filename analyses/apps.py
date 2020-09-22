from django.apps import AppConfig


class AnalysesConfig(AppConfig):
    name = 'analyses'

    def ready(self):
        import analyses.signals
