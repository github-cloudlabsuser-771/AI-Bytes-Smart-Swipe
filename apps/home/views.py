# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Capgemini Team AI Bytes
"""

import datetime

import requests
from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from google.cloud import storage

from .forms import FileUploadForm
from .request_models import UploadFileBody, GetInvoiceListBody, GetInvoiceDetailsBody

hostname = 'https://us-central1-cap-ai-bytes.cloudfunctions.net'


def create_file_upload_form(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file_instance = form.save(commit=False)
                file_instance.save()

                # Upload file to Google Cloud Storage
                client = storage.Client()
                bucket = client.get_bucket('cg-ai-bytes-bucket-1')
                blob = bucket.blob(file_instance.file.name)
                blob.upload_from_file(file_instance.file.file)

                # Generate signed URL for the uploaded file with a longer expiration time (e.g., 7 days)
                expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
                signed_url = blob.generate_signed_url(expiration=expiration_time)

                try:
                    upload_body = UploadFileBody(signed_url, request.user.username, request.user.email)
                    response = requests.post(f'{hostname}/uploadInvoice-function',
                                             data=upload_body.to_json(),
                                             headers={'Content-Type': 'application/json'})
                    if response.status_code == 200:
                        messages.success(request,
                                         f'File uploaded successfully - Status Code: {response.status_code} - OK')
                    else:
                        messages.error(request,
                                       f'File upload failed - Status Code: {response.status_code} - Something went wrong!')
                    redirect('home')  # Redirect to success page
                except Exception as e2:
                    messages.error(request, f'File upload failed on Google Cloud Function! - {str(e2)}')
                    redirect('home')  # Redirect back to home page on error
            except Exception as e1:
                messages.error(request, f'File upload failed on Google Cloud Storage! - {str(e1)}')
                redirect('home')  # Redirect back to home page on error
        return form
    else:
        return FileUploadForm()


@login_required(login_url="/login/")
def index(request):
    # form = create_file_upload_form(request)
    # if request.user.is_authenticated:
    #     get_invoice_list_body = GetInvoiceListBody(request.user.username, request.user.email)
    #     response = requests.post(f'{hostname}/getInvoiceList-function',
    #                              data=get_invoice_list_body.to_json(),
    #                              headers={'Content-Type': 'application/json'})
    #     data_list = response.json()
    #     return render(request, 'home/page-payments.html', {'form': form, 'invoices': data_list})
    # else:
    return render(request, 'home/page-payments.html')


def invoice_details(request, detail_id):
    get_invoice_details_body = GetInvoiceDetailsBody(detail_id, request.user.username, request.user.email)
    response = requests.post(f'{hostname}/getInvoiceDetail-function',
                             data=get_invoice_details_body.to_json(),
                             headers={'Content-Type': 'application/json'})
    details_data = response.json()
    return render(request, 'home/page-invoice-details.html', {'invoice_details': details_data})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
