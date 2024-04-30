# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Capgemini Team AI Bytes
"""
from django.contrib.auth import get_user_model
from django.db import models


class UploadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
User = get_user_model()


class ChatGptBot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messageInput = models.TextField()
    bot_response = models.TextField()

    def __str__(self):
        return self.user.username
