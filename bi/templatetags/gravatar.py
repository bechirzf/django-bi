import hashlib
import urllib.parse
from typing import Text

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def gravatar_url(email: Text, size: int = 40):
    """Returns url of gravatar.

    Usage example:
        {{ email|gravatar_url:150 }}

    Returns:
        A string with url of gravatar by e-mail.
    """
    return "https://www.gravatar.com/avatar/%s?%s" % (
        hashlib.md5(email.lower().encode('utf-8')).hexdigest(),
        urllib.parse.urlencode({'s': str(size)}))


@register.filter
def gravatar(email: Text, size: int = 40):
    """Returns image html tag with gravatar.

    Usage example:
        {{ email|gravatar:150 }}

    Returns:
        A string with html tag of gravatar by e-mail.
    """
    url = gravatar_url(email, size)
    return mark_safe(
        '<img src="%s" height="%d" width="%d">' % (url, size, size))
