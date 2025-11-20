# validators.py
from urllib.parse import urlparse
import ipaddress
import re

def is_valid_url(url):
    try:
        result = urlparse(url)
        if not all([result.scheme in ('http', 'https'), result.netloc]):
            return False

        if re.search(r'[\r\n\t]', url):
            return False

        host = result.hostname
        if not host:
            return False

        if host.lower() in ('localhost', '127.0.0.1', '::1'):
            return False

        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private or ip.is_loopback:
                return False
        except ValueError:
            pass

        return True
    except Exception:
        return False