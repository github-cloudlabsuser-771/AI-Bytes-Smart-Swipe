import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request


def generate_access_token():
    """
    Generates a Google Cloud access token using a service account.

    Returns:
        str: Access token string.
    """

    # Required: path to your service account JSON key file
    service_account_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    # Optional: Specify scopes if needed
    scopes = ['https://www.googleapis.com/auth/cloud-platform']

    # Load the service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key_path, scopes=scopes
    )

    # Refresh the access token
    credentials.refresh(Request())

    # Return the access token
    return credentials.token