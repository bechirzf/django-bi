from django.shortcuts import render

from bi.lib import get_entity_by_class, get_reports_list


# TODO: add decorator @login_required() to view with login required
# from django.contrib.auth.decorators import login_required


def index(request):
    # на главной странице выводится дашборд home
    dashboard = get_entity_by_class('objects.dashboards.{}.dashboard'.format('home'), 'Dashboard', request.GET)

    return render(request, 'bi/dashboard_detail.html', {'dashboard': dashboard})


def report_list(request):
    reports = get_reports_list()

    context = {'report_list': reports}

    return render(request, 'bi/list.html', context)


def report_detail(request, report_id):
    report = get_entity_by_class('objects.reports.{}.report'.format(report_id), 'Report', request.GET)

    return render(request, 'bi/report_detail.html', {'report': report})


def report_detail_raw(request, report_id):
    report = get_entity_by_class('objects.reports.{}.report'.format(report_id), 'Report', request.GET)

    return report.get_data()


def dashboard_detail(request, dashboard_id):
    dashboard = get_entity_by_class('objects.dashboards.{}.dashboard'.format(dashboard_id), 'Dashboard', request.GET)

    return render(request, 'bi/dashboard_detail.html', {'dashboard': dashboard})


def dashboard_detail_nested(request, dashboard_id, dashboard_parent_id):
    dashboard = get_entity_by_class(
        'objects.dashboards.{}.{}.dashboard'.format(dashboard_parent_id, dashboard_id), 'Dashboard', request.GET)

    return render(request, 'bi/dashboard_detail.html', {'dashboard': dashboard})
