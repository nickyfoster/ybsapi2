from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode


def vk_auth(url: str, client_secret: str) -> bool:
    """
    Checks VK App signature
    :param url: str
    :param client_secret: str
    :return: bool
    """
    query = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
    vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))

    hash_code = b64encode(HMAC(client_secret.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
    decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')

    return query["sign"] == decoded_hash_code
