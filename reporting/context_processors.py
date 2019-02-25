from .lib import get_dashboards_hierarchy_for_template


def add_variable_to_context(request):
    # получаем список дашбордов
    dashboards_hierarchy = get_dashboards_hierarchy_for_template()

    return {
        'dashboards_hierarchy': dashboards_hierarchy
    }
