from django.test import TestCase

from bi.lib import transform_python_list_to_list_for_echarts, get_entity_by_path, get_class_by_path, \
    get_dashboards_hierarchy, \
    get_dashboards_hierarchy_for_template, convert_dashboard_class_to_tuple, get_reports_list
from tests.fixtures.objects.dashboards.dummy2 import Dashboard as DummyBoard2
from tests.fixtures.objects.reports.dummy1.report import Report as DummyReport1
from tests.fixtures.objects.reports.dummy2.report import Report as DummyReport2


class LibTests(TestCase):
    def test_transform_python_list_to_list_for_echarts(self):
        self.assertEqual(transform_python_list_to_list_for_echarts([1, 2, 3]), "['1', '2', '3']")

    def test_get_class_by_path(self):
        entity = get_class_by_path('reports/dummy1/report.py', 'Report')
        self.assertEqual(str(entity), "<class 'reports.dummy1.report.Report'>")

        entity = get_class_by_path('reports/dummy100/report.py', 'Report')
        self.assertIsNone(entity)

        entity = get_class_by_path('dashboards/dummy2.py', 'Dashboard')
        self.assertEqual(str(entity), "<class 'dashboards.dummy2.Dashboard'>")

        entity = get_class_by_path('dashboards/dummy1/dummy3.py', 'Dashboard')
        self.assertEqual(str(entity), "<class 'dashboards.dummy1.dummy3.Dashboard'>")

        entity = get_class_by_path('dashboards/dummy1.py', 'Dashboard')
        self.assertEqual(str(entity), "<class 'dashboards.dummy1.Dashboard'>")

    def test_get_entity_by_path(self):
        entity = get_entity_by_path('reports/dummy1/report.py', 'Report', {})
        self.assertEqual(str(type(entity)), "<class 'reports.dummy1.report.Report'>")

        entity = get_entity_by_path('reports/dummy100/report.py', 'Report', {})
        self.assertIsNone(entity)

        entity = get_entity_by_path('dashboards/dummy2.py', 'Dashboard', {})
        self.assertEqual(str(type(entity)), "<class 'dashboards.dummy2.Dashboard'>")

        entity = get_entity_by_path('dashboards/dummy1/dummy3.py', 'Dashboard', {})
        self.assertEqual(str(type(entity)), "<class 'dashboards.dummy1.dummy3.Dashboard'>")

        entity = get_entity_by_path('dashboards/dummy1.py', 'Dashboard', {})
        self.assertEqual(str(type(entity)), "<class 'dashboards.dummy1.Dashboard'>")

    def test_get_dashboards_hierarchy(self):
        # TODO: complete test
        print(get_dashboards_hierarchy())

    def test_get_report_list(self):
        self.assertEqual([type(item) for item in get_reports_list('tests/fixtures/')],
                         [DummyReport1, DummyReport2])

    def test_dashboards_hierarchy_for_template(self):
        self.assertEqual(get_dashboards_hierarchy_for_template(),
                         {('dummy1', 'Dummy board 1', 'fa fa-pie-chart', None): [
                             ('dummy3', 'Dummy board 3', 'fa fa-pie-chart', 'dummy1')],
                             ('dummy2', 'Dummy board 2', 'fa fa-pie-chart', None): [],
                             ('home', 'home', 'fa fa-dashboard', None): []}
                         )

    def test_convert_dashboard_class_to_tuple(self):
        self.assertEqual(convert_dashboard_class_to_tuple(DummyBoard2),
                         ('dummy2', 'Dummy board 2', 'fa fa-pie-chart', None))
