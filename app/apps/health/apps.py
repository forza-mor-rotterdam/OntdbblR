from django.apps import AppConfig
from health_check.plugins import plugin_dir


class ServicesConfig(AppConfig):
    name = "apps.health"
    verbose_name = "Health"
