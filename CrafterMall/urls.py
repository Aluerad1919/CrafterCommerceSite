from django.urls import path, include
from.import views, models

urlpatterns = [
    path('', views.index),
    path('signin', views.login)
]