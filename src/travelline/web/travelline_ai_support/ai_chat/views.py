from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import AnswersFile
from .forms import AnswersFileForm
from datetime import datetime

def check_admin(user):
    return user.is_superuser

def index(request):
    return render(request, "ai_chat/base_chat.html", {"chat_box_name": "basic"})

@user_passes_test(check_admin)
def uploader(request):
    if request.method == 'POST':
        form = AnswersFileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if 'file' in dict(request.FILES).keys():
                post.filename = request.FILES['file'].name
                post.content = request.FILES['file'].open('r').read()
                print("Uploaded file")
            post.addition_date = datetime.now()
            post.save()

    form = AnswersFileForm()
    context = {
        'form': form
    }
    return render(request, "ai_chat/uploader.html", context)
