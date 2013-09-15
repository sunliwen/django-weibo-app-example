import time, json, hmac, base64, logging, hashlib
from datetime import datetime, tzinfo, timedelta

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from weibo import APIError, APIClient
from weiboapp.settings import APP_KEY, APP_SECRET, APP_URL

class AuthView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(AuthView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 
            template="auth.html",
            context=dict(
                APP_KEY=APP_KEY,
                APP_URL=APP_URL
            )
        )

    def post(self, request, *args, **kwargs):
        print request.POST

        client = _create_client()
        data = client.parse_signed_request(request.POST['signed_request'])
        print data

        user_id = data.get('uid', '')
        auth_token = data.get('oauth_token', '')
        if not user_id or not auth_token:
            return TemplateResponse(
                request, 
                template="auth.html",
                context=dict(
                    APP_KEY=APP_KEY,
                    APP_URL=APP_URL
                )
            )
        
        return HttpResponse('Hello, World!')


def _create_client(oauth_token=None, expires=None):
    client = APIClient(APP_KEY, APP_SECRET, APP_URL)
    if oauth_token and expires:
        client.set_access_token(oauth_token, expires)
    return client