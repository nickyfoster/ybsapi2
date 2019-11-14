import re

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

TOKEN_AUTH_ENABLED = False

def auth_user(user_token: str) -> bool:
    if TOKEN_AUTH_ENABLED:
        for user in User.objects.all():
            token = Token.objects.get_or_create(user=user)
            if str(token[0]) == user_token:
                return True
            else:
                continue
        return False
    else:
        return True


def get_referer_view(request, default=None):
    '''
    Return the referer view of the current request
    Example:
        def some_view(request):
            ...
            referer_view = get_referer_view(request)
            return HttpResponseRedirect(referer_view, '/accounts/login/')
    '''

    # if the user typed the url directly in the browser's address bar
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return default

    # remove the protocol and split the url at the slashes
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    if referer[0] != request.META.get('SERVER_NAME'):
        return default

    # add the slash at the relative path's view and finished
    referer = u'/' + u'/'.join(referer[1:])
    return referer
