from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import AnswersFile
from .forms import AnswersFileForm
from datetime import datetime
import pypandoc
import os

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
            post.addition_date = datetime.now()
            if 'file' in dict(request.FILES).keys():
                post.filename = request.FILES['file'].name
                format = os.path.splitext(post.filename)[-1]
                if format == '.txt':
                    post.content = request.FILES['file'].open('r').read()
                else:
                    post.content = pypandoc.convert_text(request.FILES['file'].open('r').read(), "rst", format[1:])
                post.save()
            elif post.content != "":
                if post.filename == "":
                    post.filename = "File" + str(post.addition_date)
                post.save()

    form = AnswersFileForm()
    context = {
        'form': form
    }
    return render(request, "ai_chat/uploader.html", context)
