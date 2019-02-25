from django.http import QueryDict
from django.template import Library, loader

register = Library()


@register.simple_tag
def report(report_class):
    rc = __import__(report_class, globals(), locals(), ['*'])
    cls = getattr(rc, 'Report')
    re = cls(QueryDict())

    context = {'report': re}
    template = loader.get_template('reporting/dashboard_report.html')
    return template.render(context)
