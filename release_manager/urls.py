from django.urls import path

from . import views


app_name = 'release_manager'
urlpatterns = [
    path('<int:id>/', views.release_log, name='release_log'),
]
