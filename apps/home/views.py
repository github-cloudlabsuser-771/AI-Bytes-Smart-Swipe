# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Capgemini Team AI Bytes
"""

import os
import re

import openai
from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from openai import AzureOpenAI

from .models import ChatGptBot

# hostname = 'https://us-central1-cap-ai-bytes.cloudfunctions.net'

openai.api_type = "azure"
# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
openai.api_version = "2024-02-15-preview"

# Azure OpenAI setup
openai.api_base = "https://testing1310.openai.azure.com/"  # Add your endpoint here
openai.api_key = os.getenv("OPENAI_API_KEY")  # Add your OpenAI API key here
deployment_id = "testing0613"  # Add your deployment ID here

# Azure AI Search setup
search_endpoint = "https://testingsearch1310.search.windows.net"  # Add your Azure AI Search endpoint here
search_key = os.getenv("SEARCH_KEY")  # Add your Azure AI Search admin key here
search_index_name = "paisa-bazar-credit-cards-search-index"  # Add your Azure AI Search index name here

client = AzureOpenAI(
    base_url=f"{openai.api_base}openai/deployments/{deployment_id}/extensions",
    api_version='2023-08-01-preview',
    api_key=os.environ['OPENAI_API_KEY']
)

system_message_content = "You are an Expert financial advisor and help users to get maximum credit cards benefits. From search index do not show any document references and be concise to provide responses properly either in bullet points in html text format."


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
                    model=deployment_id,
                    # Send all messages from current session
                    messages=[
                        {
                            "role": "system",
                            "content": system_message_content
                        },
                        {
                            "role": "user",
                            "content": clean_user_input,
                        }
                    ],
                    # Controls randomness of response
                    temperature=0,
                    # Set a limit on the number of tokens per genai response
                    max_tokens=500,
                    # Similar to temperature, this controls randomness but uses a different method
                    top_p=0.5,
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
                                    "key": search_key,
                                    "semantic_configuration": "default",
                                    "query_type": "simple",
                                    "fields_mapping": {},
                                    "in_scope": True,
                                    "role_information": system_message_content,
                                    "filter": None,
                                    "strictness": 3,
                                    "top_n_documents": 5,
                                }
                            }
                        ]
                    }
                )
                # get response from bot
                bot_response = response.choices[0].message.content
                replacement_text = ""
                updated_bot_response = replace_doc_strings(bot_response, replacement_text)
                print(updated_bot_response)
                obj, created = ChatGptBot.objects.get_or_create(
                    user=request.user,
                    messageInput=clean_user_input,
                    bot_response=updated_bot_response,
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


def replace_doc_strings(original_string, replacement_string):
    # Define the pattern to match strings like '[doc1]', '[doc2]', etc.
    pattern = r'\s*\[doc\d+\]'

    # Use re.sub() to replace matched patterns with the replacement string
    modified_string = re.sub(pattern, replacement_string, original_string)

    return modified_string


@login_required
def delete_history(request):
    chat_gpt_objs = ChatGptBot.objects.filter(user=request.user)
    chat_gpt_objs.delete()
    messages.success(request, "All messages have been deleted")
    return redirect(request.META['HTTP_REFERER'])


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
