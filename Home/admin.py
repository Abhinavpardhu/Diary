from django.contrib import admin
from .models import DiaryEntry, Tag

admin.site.register(DiaryEntry)
admin.site.register(Tag)