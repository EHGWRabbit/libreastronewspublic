from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_time_stamp_path 
from django.db.models.signals import post_save 
from .utilities import send_new_comment_notification


class AstroUser(AbstractUser):
    #прошел ли активацию
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    #спрашиваем об уведомлениях
    send_messages = models.BooleanField(default=True, verbose_name='рисылать мне оповещения о новых комментариях')

    #добавляем возможность удаления всех связанных с
    #юзером данных
    def delete(self, *args, **kwargs):
        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


#модель рубрикации
class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, 
                    null=True, blank=True, verbose_name='Надрубрика')


#менеджер записей подрубрик
class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)#переопределяем метод для выбора только super_rubric

#класс суперрубрикации
class SuperRubric(Rubric):
    objects = SuperRubricManager()


    def __str__(self):
        return self.name
    
    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'

#класс менеджера перебора записей субрубрик
class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)#моедернизтируем код с помощью переопределения метода get_queryset()



#класс подрубрик
class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


#модель для выгрузки файлов
class Bb(models.Model):
    #подрубрика
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика новостей')
    #название новости
    title = models.CharField(max_length=100, verbose_name='Краткое название')
    #содержание новости
    content = models.TextField(verbose_name='Сама новость')
    #источник новости
    source = models.CharField(max_length=40, verbose_name='Источник новости')
    #контакты автора
    #contacts = models.CharField(max_length=40, verbose_name='Связаться с автором новости')
    #изображение 
    image = models.ImageField(blank=True, upload_to=get_time_stamp_path, verbose_name='Изображение к новости')
    #актор новости
    author = models.ForeignKey(AstroUser, on_delete=models.CASCADE, verbose_name='Автор новости')
    #показывать ли новость в списке
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводит в списке?')
    #новость опублекована
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опублекована')

    #переопределение метода delete для удаления всех иллюстраций
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs) 

    class Meta:
        verbose_name_plural = 'Новости астрономии'
        verbose_name = 'Новости'
        ordering = ['-created_at']

#модель дополнительных иллюстраций
class AdditionalImage(models.Model):
    #новость, к которой относиться изображение
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Новости')
    #сама иллюстрация
    image = models.ImageField(upload_to=get_time_stamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные изображения'
        verbose_name = 'Дополнительное изображение'


#модель сомментариев к новостям
class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Новость')
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание комментария')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Вывести на экран?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опублекован')

    class Meta:
        verbose_name_plural = 'Комментарии пользователей'
        verbose_name = 'Комментарии'
        ordering = ['created_at'] 

'''
#функция отправки уведомлений о новых коммент ариях
def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].bb.author 
    if kwargs['created'] and author.send_messages:
        send_new_comment_notification(kwargs['instance'])
post_save.connect(post_save_dispatcher, sender=Comment)
'''