from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class DiaryEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('sad', '😢 Sad'),
        ('calm', '😌 Calm'),
        ('energetic', '⚡ Energetic'),
        ('angry', '😠 Angry'),
        ('anxious', '😰 Anxious'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='calm')
    favorite = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name='entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Diary Entries"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
