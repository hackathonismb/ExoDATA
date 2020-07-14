from django.db import models

# Create your models here.
class Score(models.Model):
    data = models.FileField(max_length=500)
