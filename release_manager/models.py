from django.db import models


class ReleaseLog(models.Model):
    """リリース履歴を保持する

    """
    date = models.DateField(unique=True, verbose_name='リリース日')
    title = models.CharField(max_length=32, unique=True, verbose_name='リリース概要')
    description = models.TextField(max_length=400, verbose_name='リリース内容')

    class Meta:
        verbose_name = verbose_name_plural = 'リリース履歴'

    def __str__(self):
        return str(self.date)
