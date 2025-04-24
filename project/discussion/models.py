from asyncio import Event
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва події")
    description = models.TextField(verbose_name="Опис події")
    date = models.DateTimeField(verbose_name="Дата та час події")
    location = models.CharField(max_length=200, verbose_name="Місце проведення")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events', verbose_name="Організатор")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Подія"
        verbose_name_plural = "Події"
        ordering = ['-date']

# Потім визначаємо клас Comment
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments', verbose_name="Подія")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    text = models.TextField(verbose_name="Текст коментаря")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Коментар від {self.author.username} до події {self.event.title}'

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"
        ordering = ['-created_at']

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.event.title}"