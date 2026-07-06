from django.db import models

class page(models.Model):
    DAT=models.DateTimeField("")
    content=models.CharField(max_length=700)
