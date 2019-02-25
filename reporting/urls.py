from django.urls import path

from . import views

app_name = 'reporting'
urlpatterns = [
    # example: /
    path('', views.index, name='index'),
    # example: /reports/
    path('reports/', views.report_list, name='report-list'),
    # example: /reports/Dummy/
    path('reports/<report_id>/', views.report_detail, name='report-detail'),
    # example: /reports/Dummy/raw/
    path('reports/<report_id>/raw/', views.report_detail_raw, name='report-detail-raw'),
    # example: /dashboards/Dummy/
    path('dashboards/<dashboard_id>/', views.dashboard_detail, name='dashboard-detail'),
    # example: /dashboards/Dummy/DummyReport1/
    path('dashboards/<dashboard_parent_id>/<dashboard_id>/', views.dashboard_detail_nested,
         name='dashboard-detail-nested'),
]
