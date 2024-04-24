from django.db import models

class AnswersFile(models.Model):
    filename = models.TextField('filename')
    content = models.TextField('content')
    addition_date = models.DateTimeField("datetime")

    def __str__(self):
        return self.filename
