from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


# もろもろの設定
def has_delete_permission(self, request, obj=None):
    if request.user.is_superuser:
        return True
    else:
        return False


admin.site.unregister(Group)
admin.site.disable_action('delete_selected')
admin.ModelAdmin.has_delete_permission = has_delete_permission


class BaseAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """ChoiceField横の編集ボタンを非表示にする

        """
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        formfield.widget.can_add_related = False
        formfield.widget.can_change_related = False
        formfield.widget.can_delete_related = False

        return formfield


class LunchGenreInlineAdmin(admin.TabularInline):
    model = models.LunchPlace.genre.through

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """ChoiceField横の編集ボタンを非表示にする

        """
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if formfield:
            formfield.widget.can_add_related = True
            formfield.widget.can_change_related = False
            formfield.widget.can_delete_related = False
        return formfield


@admin.register(models.District)
class DistrictAdmin(BaseAdmin):
    # list
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    # detail
    fields = [
        'id', 'name',
    ]
    readonly_fields = ('id',)


@admin.register(models.StoreType)
class StoreTypeAdmin(BaseAdmin):
    # list
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    # detail
    fields = [
        'id', 'name', 'description',
    ]
    readonly_fields = ('id',)


@admin.register(models.LunchGenre)
class LunchGenreAdmin(BaseAdmin):
    # list
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    # detail
    fields = [
        'id', 'name',
    ]
    readonly_fields = ('id',)


@admin.register(models.LunchPlace)
class LunchPlaceAdmin(BaseAdmin):
    # list
    list_display = ('id', 'name', 'district', 'store_type', 'is_valid', 'has_eatin', 'has_takeout')
    list_display_links = ('id', 'name')
    list_filter = ('is_valid', 'genre', 'store_type')
    search_fields = ('name',)
    ordering = ('id',)
    # detail
    fields = [
        'id', 'name', 'district', 'store_type', 'is_valid', 'has_eatin', 'has_takeout',
    ]
    inlines = (
        LunchGenreInlineAdmin,
    )
    readonly_fields = ('id',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('genre')
        return queryset
