from django.db import models
from django.utils import timezone

class pag(models.Model):
    DAT=models.DateField(default=timezone.now())
    content=models.TextField(max_length=700)
