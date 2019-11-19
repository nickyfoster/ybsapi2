import copy
import json
import re
from json import JSONDecodeError
from pathlib import Path

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


def load_json(file):
    file = Path(file)
    try:
        with file.open() as f:
            d = json.load(f)
    except (FileNotFoundError, JSONDecodeError) as e:
        d = dict()

    return d


def get_config():
    # TODO add paths
    source_config = load_json(Path(__file__).parent / '..' / 'main.json')
    etc_config = load_json('path/to/conf')

    source_config.update(etc_config)

    return source_config


def get_option_from_nlu_config(option_path: List[str], default_value=None, config=None):
    config = get_config() if config is None else config

    if isinstance(option_path, str):
        option_path = [option_path]

    d = copy.deepcopy(config)

    for k in option_path:
        try:
            d = d[k]
        except KeyError:
            return default_value

    return d
