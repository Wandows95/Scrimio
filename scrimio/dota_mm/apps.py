from django.apps import AppConfig
from .app_settings import APP_NAME

class DotaMmConfig(AppConfig):
	# Tie name automatically to app_settings APP_NAME
    name = APP_NAME