from django.db import models
from django.contrib.auth.models import AbstractUser


class AstroUser(AbstractUser):
    #прошел ли активацию
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    #спрашиваем об уведомлениях
    send_messages = models.BooleanField(default=True, verbose_name='рисылать мне оповещения о новых комментариях')

    class Meta(AbstractUser.Meta):
        pass
