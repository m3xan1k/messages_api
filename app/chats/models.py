from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return f'<Contact {self.user.username}>'


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='messages', null=True)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<Message {self.author.username} in {self.chat}>'


class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='chats')
