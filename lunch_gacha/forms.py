from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count

from . import models
from .widgets import CustomCheckboxSelectMultiple


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class GachaForm(forms.Form):
    """ガチャを引くフォーム

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'custom-checkbox'

    district = forms.ModelMultipleChoiceField(
        label='地区',
        queryset=models.District.objects.annotate(
            Count('lunchplace')).filter(lunchplace__count__gte=1),
        widget=CustomCheckboxSelectMultiple,
        required=False,
    )

    genre = forms.ModelMultipleChoiceField(
        label='ジャンル',
        queryset=models.LunchGenre.objects.annotate(
            Count('lunchplace')).filter(lunchplace__count__gte=1),
        widget=CustomCheckboxSelectMultiple,
        required=False,
    )


class PlaceAppendForm(forms.ModelForm):
    """ガチャ要素を追加するフォーム

    """

    class Meta:
        model = models.LunchPlace
        fields = ('name', 'district', 'genre')
