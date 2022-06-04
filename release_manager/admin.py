from django.contrib import admin

from lunch_gacha.admin import BaseAdmin
from . import models


@admin.register(models.ReleaseLog)
class ReleaseLogAdmin(BaseAdmin):
    # list
    list_display = ('date', 'title')
    list_display_links = ('date', 'title')
    search_fields = ('title', 'description')
    # detail
    fields = [
        'date', 'title', 'description',
    ]
