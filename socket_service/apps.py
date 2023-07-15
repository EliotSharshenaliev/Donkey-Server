from django.apps import AppConfig


class SocketServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socket_service'

    def ready(self):
        import socket_service.signals