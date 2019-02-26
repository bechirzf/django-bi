from django.conf import settings
from django.http import QueryDict
from django.template import Library, loader

register = Library()


@register.simple_tag
def report(report_class):
    splitted_objects_path = settings.OBJECTS_PATH.split('/')
    splitted_objects_path = splitted_objects_path[:-1]

    if len(splitted_objects_path):
        report_class = '.'.join(splitted_objects_path) + '.' + report_class

    rc = __import__(report_class, globals(), locals(), ['*'])
    cls = getattr(rc, 'Report')
    re = cls(QueryDict())

    context = {'report': re}
    template = loader.get_template('bi/dashboard_report.html')
    return template.render(context)
