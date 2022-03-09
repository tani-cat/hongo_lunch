from django.urls import path

from . import views


app_name = 'lunch_gacha'
urlpatterns = [
    path('gacha/', views.GachaView.as_view(), name='gacha'),
    path('result/', views.GachaResultView.as_view(), name='result'),
    path('list/', views.GachaListView.as_view(), name='list'),
]
