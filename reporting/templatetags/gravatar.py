import hashlib
import urllib.parse

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def gravatar_url(email, size=40):
    """
    Возвращает только урл граватара.

    Пример использования: {{ email|gravatar_url:150 }}

    :param email:
    :param size:
    :return:
    """
    return "https://www.gravatar.com/avatar/%s?%s" % (
        hashlib.md5(email.lower().encode('utf-8')).hexdigest(), urllib.parse.urlencode({'s': str(size)}))


@register.filter
def gravatar(email, size=40):
    """
    Возвращает image tag граватара.

    Пример использования:  {{ email|gravatar:150 }}

    :param email:
    :param size:
    :return:
    """
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))
