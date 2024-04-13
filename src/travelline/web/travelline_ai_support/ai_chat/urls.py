from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("<str:chat_box_name>/", views.chat_box, name="room"),
]