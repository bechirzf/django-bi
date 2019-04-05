from django.urls import path, re_path

from . import views

app_name = 'bi'
urlpatterns = [
    # example: /
    path('', views.index, name='index'),
    # example: /reports/
    path('reports/', views.report_list, name='report-list'),
    # example: /reports/Dummy/raw/
    re_path(
        r'reports/(?P<report_path>.+)/raw/$',
        views.report_detail_raw,
        name='report-detail-raw'),
    # example: /reports/Dummy/
    re_path(
        r'reports/(?P<report_path>.+)/$',
        views.report_detail,
        name='report-detail'),
    # example: /dashboards/Dummy/
    path(
        'dashboards/<dashboard_id>/',
        views.dashboard_detail,
        name='dashboard-detail'),
    # example: /dashboards/Dummy/DummyReport1/
    path(
        'dashboards/<dashboard_parent_id>/<dashboard_id>/',
        views.dashboard_detail_nested,
        name='dashboard-detail-nested'),
    # example: /api/flush-cache/
    path('api/flush-cache/', views.flush_cache, name='flush-cache'),
]
