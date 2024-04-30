# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Capgemini Team AI Bytes
"""

from django.urls import path, re_path

from apps.home import views

urlpatterns = [

    # Path to Home (Invoices also loaded on the same page)
    path('', views.index, name='home'),

    # Path to Delete Chats
    path("delete/", views.delete_history, name='deleteChat'),

    # Path to Invoice Details
    # path('invoice/<detail_id>', views.invoice_details, name='invoice_details'),

    # Path with regex to match other all pages
    re_path(r'^.*\.*', views.pages, name='pages'),
]
