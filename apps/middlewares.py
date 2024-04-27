from django.utils.deprecation import MiddlewareMixin
from .access import generate_access_token


class CustomHeadersMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Add common headers to API requests
        if request.path.startswith('/us-central1-cap-ai-bytes.cloudfunctions.net/'):
            access_token = generate_access_token()
            print(f'Access Token: {access_token}')
            request.headers['Content-Type'] = 'application/json'
            request.headers['Authorization'] = f'Bearer {access_token}'
        return None
