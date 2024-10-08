from django.db import models


class Notification(models.Model):
    """Модель уведомления"""
    text = models.TextField()
    event_link = models.URLField(
        max_length=128, 
        null=True,
        default=None,
        verbose_name='Ссылка на событие'
    )
    receiver_id = models.UUIDField(
        db_index=True,
        editable=False,
        verbose_name='ID получателя'
    ) 
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ('-time_create', )
        
    def __str__(self):
        return f'{self.receiver_id} - {self.text}'