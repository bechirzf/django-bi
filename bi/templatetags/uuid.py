from typing import Text
from uuid import uuid4

from django.template import Library, Node, TemplateSyntaxError

register = Library()


class UUIDNode(Node):
    """
    Генерация UUID.
    """

    def __init__(self, var_name: Text):
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = str(uuid4())
        return ''


def do_uuid(parser, token):
    """
    Генерация UUID

    Использование:
        {% uuid var_name %}
        var_name будет содержать сгенерированный UUID
    """
    try:
        tag_name, var_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            "%r tag requires exactly one argument" % token.contents.split()[0])
    return UUIDNode(var_name)


do_uuid = register.tag('uuid', do_uuid)
