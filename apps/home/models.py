# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Capgemini Team AI Bytes
"""

from django.db import models


class UploadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
