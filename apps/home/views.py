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
import os
import openai
from openai import AzureOpenAI
from .models import ChatGptBot
from .forms import FileUploadForm
from .request_models import UploadFileBody, GetInvoiceListBody, GetInvoiceDetailsBody

# hostname = 'https://us-central1-cap-ai-bytes.cloudfunctions.net'

openai.api_type = "azure"
# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
openai.api_version = "2023-08-01-preview"

# Azure OpenAI setup
openai.api_base = "https://testing1310.openai.azure.com/"  # Add your endpoint here
openai.api_key = os.getenv("OPENAI_API_KEY")  # Add your OpenAI API key here
# deployment_id = "testing0613"  # Add your deployment ID here

# Azure AI Search setup
search_endpoint = "https://testingsearch1310.search.windows.net"  # Add your Azure AI Search endpoint here
search_key = os.getenv("SEARCH_KEY")  # Add your Azure AI Search admin key here
search_index_name = "paisa-bazar-credit-cards-index"  # Add your Azure AI Search index name here

gen_ai_model_name = 'testing0613'

client = AzureOpenAI(
    base_url=f"{openai.api_base}openai/deployments/{gen_ai_model_name}/extensions",
    api_version='2023-08-01-preview',
    api_key=os.environ['OPENAI_API_KEY']
)


def index(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        if request.method == 'POST':
            # get user input from the form
            user_input = request.POST.get('userInput')
            # clean input from any white spaces
            clean_user_input = str(user_input).strip()
            # send request with user's prompt
            try:
                response = client.chat.completions.create(
                    # Replace with the actual genai name if it exists
                    model=gen_ai_model_name,
                    # Send all messages from current session
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert financial advisor and help peoples to get the maximum credit card benefits."
                        },
                        {
                            "role": "user",
                            "content": clean_user_input,
                        }
                    ],
                    # Controls randomness of response
                    temperature=0.8,
                    # Set a limit on the number of tokens per genai response
                    max_tokens=2000,
                    # Similar to temperature, this controls randomness but uses a different method
                    top_p=0.95,
                    # Reduce the chance of repeating a token proportionally based on how often it has appeared in the text so far
                    frequency_penalty=0,
                    # Reduce the chance of repeating any token that has appeared in the text at all so far
                    presence_penalty=0,
                    # Number of completions
                    n=1,
                    # Make the genai end its response at a desired point
                    stop=None,
                    extra_body={
                        "dataSources": [
                            {
                                "type": "AzureCognitiveSearch",
                                "parameters": {
                                    "endpoint": search_endpoint,
                                    "indexName": search_index_name,
                                    "key": search_key
                                }
                            }
                        ]
                    }
                )
                # get response

                bot_response = response.choices[0].message.content

                obj, created = ChatGptBot.objects.get_or_create(
                    user=request.user,
                    messageInput=clean_user_input,
                    bot_response=bot_response,
                )
            except openai.APIConnectionError as e:
                # Handle connection error here
                messages.warning(request, f"Failed to connect to OpenAI API, check your internet connection")
            except openai.RateLimitError as e:
                # Handle rate limit error (we recommend using exponential backoff)
                messages.warning(request,
                                 f"You exceeded your current quota, please check your plan and billing details.")
                messages.warning(request, f"If you are a developper change the API Key")

            return redirect(request.META['HTTP_REFERER'])
        else:
            # retrieve all messages belong to logged in user
            get_history = ChatGptBot.objects.filter(user=request.user)
            context = {'get_history': get_history}
            return render(request, 'home/page-chat.html', context)
    else:
        return redirect("login")


@login_required
def delete_history(request):
    chat_gpt_objs = ChatGptBot.objects.filter(user=request.user)
    chat_gpt_objs.delete()
    messages.success(request, "All messages have been deleted")
    return redirect(request.META['HTTP_REFERER'])


# def create_file_upload_form(request):
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 file_instance = form.save(commit=False)
#                 file_instance.save()
#
#                 # Upload file to Google Cloud Storage
#                 client = storage.Client()
#                 bucket = client.get_bucket('cg-ai-bytes-bucket-1')
#                 blob = bucket.blob(file_instance.file.name)
#                 blob.upload_from_file(file_instance.file.file)
#
#                 # Generate signed URL for the uploaded file with a longer expiration time (e.g., 7 days)
#                 expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=7)
#                 signed_url = blob.generate_signed_url(expiration=expiration_time)
#
#                 try:
#                     upload_body = UploadFileBody(signed_url, request.user.username, request.user.email)
#                     response = requests.post(f'{hostname}/uploadInvoice-function',
#                                              data=upload_body.to_json(),
#                                              headers={'Content-Type': 'application/json'})
#                     if response.status_code == 200:
#                         messages.success(request,
#                                          f'File uploaded successfully - Status Code: {response.status_code} - OK')
#                     else:
#                         messages.error(request,
#                                        f'File upload failed - Status Code: {response.status_code} - Something went wrong!')
#                     redirect('home')  # Redirect to success page
#                 except Exception as e2:
#                     messages.error(request, f'File upload failed on Google Cloud Function! - {str(e2)}')
#                     redirect('home')  # Redirect back to home page on error
#             except Exception as e1:
#                 messages.error(request, f'File upload failed on Google Cloud Storage! - {str(e1)}')
#                 redirect('home')  # Redirect back to home page on error
#         return form
#     else:
#         return FileUploadForm()


# @login_required(login_url="/login/")
# def index(request):
#     # form = create_file_upload_form(request)
#     # if request.user.is_authenticated:
#     #     get_invoice_list_body = GetInvoiceListBody(request.user.username, request.user.email)
#     #     response = requests.post(f'{hostname}/getInvoiceList-function',
#     #                              data=get_invoice_list_body.to_json(),
#     #                              headers={'Content-Type': 'application/json'})
#     #     data_list = response.json()
#     #     return render(request, 'home/page-payments.html', {'form': form, 'invoices': data_list})
#     # else:
#     return render(request, 'home/page-chat.html')


# def invoice_details(request, detail_id):
#     get_invoice_details_body = GetInvoiceDetailsBody(detail_id, request.user.username, request.user.email)
#     response = requests.post(f'{hostname}/getInvoiceDetail-function',
#                              data=get_invoice_details_body.to_json(),
#                              headers={'Content-Type': 'application/json'})
#     details_data = response.json()
#     return render(request, 'home/page-invoice-details.html', {'invoice_details': details_data})


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
