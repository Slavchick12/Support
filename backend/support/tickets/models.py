from django.db import models

from users.models import User

from .utils import STATUSES, UNRESOLVED


class Ticket(models.Model):
    topic = models.CharField('тема', max_length=50, help_text='Задайте тему')
    descripion = models.TextField('описание', help_text='Опишите проблему')
    file = models.FileField(upload_to='files', null=True, blank=True)
    status = models.CharField(
        'статус', choices=STATUSES, default=UNRESOLVED, max_length=30
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='client',
        verbose_name='клиент',
    )
    date = models.DateTimeField('дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self):
        return f'{self.topic}'


class TicketResponse(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, related_name='ticket',
        verbose_name='обращение'
    )
    message = models.ForeignKey(  # Сообщение, на которое можно ответить
        'self', on_delete=models.CASCADE, related_name='messages',
        verbose_name='ответ', null=True, blank=True
    )
    text = models.TextField('текст', help_text='Здесь Ваш текст')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='responding',
        verbose_name='ответчик'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.ticket}'
