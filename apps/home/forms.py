# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Capgemini Team AI Bytes
"""

from django import forms

from .models import UploadedFile


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
