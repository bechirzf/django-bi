from .lib import get_dashboards_hierarchy_for_template


def add_variable_to_context(request):
    # получаем список дашбордов
    dashboards_hierarchy = get_dashboards_hierarchy_for_template()

    import pkg_resources
    bi_version = pkg_resources.get_distribution("django-bi").version

    return {
        'dashboards_hierarchy': dashboards_hierarchy,
        'bi_version': bi_version
    }
