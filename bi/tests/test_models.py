from django.http import QueryDict
from django.test import TestCase

from bi.tests.fixtures.objects.dashboards.dummy1.dashboard import Dashboard as DummyBoard1
from bi.tests.fixtures.objects.dashboards.dummy1.dummy3.dashboard import Dashboard as DummyBoard3
from bi.tests.fixtures.objects.reports.dummy1.report import Report as DummyReport1


class DashboardTests(TestCase):
    def test_id(self):
        board = DummyBoard1(QueryDict())
        self.assertEqual(board.id, 'dummy1')

    def test_template(self):
        board = DummyBoard1(QueryDict())
        self.assertEqual(board.template, 'dashboards/dummy1/template.html')

    def test_get_parent_dashboard_id(self):
        self.assertEqual(DummyBoard3.get_parent_dashboard_id(), 'dummy1')
        self.assertIsNone(DummyBoard1.get_parent_dashboard_id())

    def test_get_parent_dashboard_class(self):
        self.assertEqual(DummyBoard3.get_parent_dashboard_class(), DummyBoard1)


class ReportTests(TestCase):
    def test_id(self):
        dr1 = DummyReport1(QueryDict())
        self.assertEqual(dr1.id, 'dummy1')

    def test_template(self):
        dr1 = DummyReport1(QueryDict())
        self.assertEqual(dr1.template, 'reports/dummy1/template.html')

    def test_container_id(self):
        dr1 = DummyReport1(QueryDict())
        self.assertEqual(dr1.container_id, 'dummy1_report')
