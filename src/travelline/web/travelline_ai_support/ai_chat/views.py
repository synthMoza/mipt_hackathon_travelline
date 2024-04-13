from django.shortcuts import render


def index(request):
    return render(request, "ai_chat/base_chat.html", {"chat_box_name": "basic"})


def chat_box(request, chat_box_name):
    return render(request, "ai_chat/base_chat.html", {"chat_box_name": chat_box_name})
