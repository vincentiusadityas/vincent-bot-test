# echobot / urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    url('^callback/', views.callback),
]