from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
        verbose_name='Прошел активацию?')
    # send_messages = models.BooleanField(default=True,
    #     verbose_name='Слать оповещения о новых комментариях?')

    def delete(self, *args, **kwargs):
        for todo in self.todo_set.all():
            todo.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


from django.dispatch import Signal
from .utilities import send_activation_notification

user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispatcher)


class ToDo(models.Model):
    description = models.CharField(max_length=40, verbose_name='Описание')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор')
    is_important = models.BooleanField(default=False, db_index=True, verbose_name='Важное?')
    is_completed = models.BooleanField(default=False, db_index=True, verbose_name='Завершено?')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Задания'
        verbose_name = 'Задание'
        ordering = ['-created_at']
