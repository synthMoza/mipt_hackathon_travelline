from .models import AnswersFile
from django.forms import ModelForm, TextInput, Textarea, FileInput, FileField


class AnswersFileForm(ModelForm):

    file = FileField(required=False)

    class Meta:
        model = AnswersFile
        fields = ["filename", "content", "file"]
        widgets = {
            "filename": TextInput(attrs={
                'class': 'form-control',
                "name":"question",
                "id":"InputName",
                "placeholder":"Enter file name",
            }),
            "content": Textarea(attrs={
                'class':"form-control",
                'id':"InputAnswer", 
                'placeholder':"Enter content",
                'rows':"20",
                'style':"overflow:hidden",
            }),
            "file": FileInput(attrs={
                "type":"file",
                "name":"file"
            })
        }