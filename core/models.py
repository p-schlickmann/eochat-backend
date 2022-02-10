from django.contrib.auth import get_user_model
from django.db import models

from core.utils import generate_random_integer


class Chat(models.Model):
    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} | {self.code}'

    def save(self, *args, **kwargs):
        if not self.code:
            new_code = generate_random_integer()
            while Chat.objects.filter(code=new_code).exists():
                new_code = generate_random_integer()
            self.code = new_code
        super(Chat, self).save(*args, **kwargs)


class Message(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='own_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} | {self.content} | {self.chat}'
