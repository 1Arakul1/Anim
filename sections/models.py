#sections\models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Section(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sections')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"


class Content(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    file = models.FileField(upload_to='content_files/', blank=True, null=True) # Или ImageField
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Содержимое"
        verbose_name_plural = "Содержимое"
