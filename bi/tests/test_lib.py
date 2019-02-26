from django.test import TestCase

from bi.lib import transform_python_list_to_list_for_echarts, get_entity_by_class, get_dashboards_hierarchy, \
    get_dashboards_hierarchy_for_template, convert_dashboard_class_to_tuple, get_reports_list
from bi.tests.fixtures.objects.dashboards.dummy1.dashboard import Dashboard as DummyBoard1
from bi.tests.fixtures.objects.dashboards.dummy1.dummy3.dashboard import Dashboard as DummyBoard3
from bi.tests.fixtures.objects.dashboards.dummy2.dashboard import Dashboard as DummyBoard2
from bi.tests.fixtures.objects.reports.dummy1.report import Report as DummyReport1
from bi.tests.fixtures.objects.reports.dummy2.report import Report as DummyReport2


class LibTests(TestCase):
    def test_transform_python_list_to_list_for_echarts(self):
        self.assertEqual(transform_python_list_to_list_for_echarts([1, 2, 3]), "['1', '2', '3']")

    def test_get_entity_by_class(self):
        entity = get_entity_by_class('bi.tests.fixtures.objects.reports.dummy1.report', 'Report', {})
        self.assertEqual(type(entity), DummyReport1)

    def test_get_dashboards_hierarchy(self):
        self.assertEqual(
            {DummyBoard1: [DummyBoard3], DummyBoard2: []},
            get_dashboards_hierarchy('bi/tests/fixtures/'))

    def test_get_report_list(self):
        self.assertEqual([type(item) for item in get_reports_list('bi/tests/fixtures/')],
                         [DummyReport1, DummyReport2])

    def test_dashboards_hierarchy_for_template(self):
        self.assertEqual(get_dashboards_hierarchy_for_template('bi/tests/fixtures/'),
                         {('dummy1', 'Dummy board 1', 'fa fa-pie-chart', None): [
                             ('dummy3', 'Dummy board 3', 'fa fa-pie-chart', 'dummy1')],
                             ('dummy2', 'Dummy board 2', 'fa fa-pie-chart', None): []}
                         )

    def test_convert_dashboard_class_to_tuple(self):
        self.assertEqual(convert_dashboard_class_to_tuple(DummyBoard1),
                         ('dummy1', 'Dummy board 1', 'fa fa-pie-chart', None))
