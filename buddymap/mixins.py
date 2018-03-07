from django.utils.http import is_safe_url
from oauth2_provider.models import AccessToken
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.settings import api_settings
from urllib import parse

class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class RedirectNextMixin(object):
    default_next='/'
    def get_next_url(self):
        request = self.request
        if(is_safe_url(request.GET.get('next') or request.POST.get('next') or None, request.get_host())):
            return redirect_path
        return self.default_next

#########################
#Channels Auth Middleware
#########################
authenticators = [auth() for auth in api_settings.DEFAULT_AUTHENTICATION_CLASSES]
class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        """
            input: query string params
            process: authenticate user and return the user
        """
        params = { key.decode(): val[0].decode() for key, val in parse.parse_qs(scope['query_string']).items()}
        if(params.get('token')):
            try:
                atok = AccessToken.objects.get(token = params.get('token'))
                scope["user"] = atok.user
            except AccessToken.DoesNotExist:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()
        # Return the inner application directly and let it run everything else
        return self.inner(scope)
