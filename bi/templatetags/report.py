from django.http import QueryDict
from django.template import Library, loader

from bi.lib import get_entity_by_path

register = Library()


@register.simple_tag
def report(report_class):
    rprt = get_entity_by_path('reports/{}'.format(report_class), 'Report', QueryDict())
    context = {'report': rprt}
    template = loader.get_template('bi/dashboard_report.html')
    return template.render(context)
