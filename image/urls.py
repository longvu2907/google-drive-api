from django.shortcuts import redirect
from django.urls import path, re_path

from image.views import ImageListView

urlpatterns = [
  re_path(r'^image/(?P<folder>.+)/$', ImageListView.as_view()),
  re_path(r'^image/$', ImageListView.as_view())
]