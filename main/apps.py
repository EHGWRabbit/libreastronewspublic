from django.apps import AppConfig
from django.dispatch import Signal#обьявляем сигнал и привязываем к нему оьработчик
from .utilities import send_activation_note

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Новости астрономии'


user_registered = Signal(providing_args=['instance']) 

def user_registered_dispatcher(sender, **kwargs):
    send_activation_note(kwargs['instance'])

user_registered.connect(user_registered_dispatcher)