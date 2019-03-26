from os.path import normcase

from django.test import TestCase

from bi.lib import get_entity_by_path, get_class_by_path
from tests.fixtures.objects.reports.dummy.dummy3 import Report as DummyReport3
from tests.fixtures.objects.reports.dummy1 import Report as DummyReport1


class DashboardTests(TestCase):
    def test_id(self):
        board = get_entity_by_path('dashboards/dummy1.py', 'Dashboard', {})
        self.assertEqual(board.id, 'dummy1')

    def test_template(self):
        board = get_entity_by_path('dashboards/dummy1.py', 'Dashboard', {})
        self.assertEqual(board.template, normcase('dashboards/dummy1.html'))

    def test_get_parent_dashboard_id(self):
        board = get_entity_by_path('dashboards/dummy1.py', 'Dashboard', {})
        self.assertIsNone(board.get_parent_dashboard_id())
        board = get_entity_by_path('dashboards/dummy1/dummy3.py', 'Dashboard', {})
        self.assertEqual(board.get_parent_dashboard_id(), 'dummy1')

    def test_get_parent_dashboard_class(self):
        dummy_board3 = get_class_by_path('dashboards/dummy1/dummy3.py', 'Dashboard')
        dummy_board1 = get_class_by_path('dashboards/dummy1.py', 'Dashboard')
        self.assertEqual(str(dummy_board3.get_parent_dashboard_class()), str(dummy_board1))

    def test_get_parent_dashboard(self):
        dummy_board3_class = get_class_by_path('dashboards/dummy1/dummy3.py', 'Dashboard')
        self.assertEqual(str(type(dummy_board3_class.get_parent_dashboard())), "<class 'dashboards.dummy1.Dashboard'>")

    def test_has_parent_dashboard(self):
        dummy_board1 = get_class_by_path('dashboards/dummy1.py', 'Dashboard')
        self.assertFalse(dummy_board1.has_parent_dashboard())
        dummy_board3 = get_class_by_path('dashboards/dummy1/dummy3.py', 'Dashboard')
        self.assertTrue(dummy_board3.has_parent_dashboard())

    def test_get_parent_dashboard_url(self):
        dummy_board1 = get_class_by_path('dashboards/dummy1.py', 'Dashboard')
        self.assertIsNone(dummy_board1.get_parent_dashboard_url())
        dummy_board3 = get_class_by_path('dashboards/dummy1/dummy3.py', 'Dashboard')
        self.assertEqual(dummy_board3.get_parent_dashboard_url(), '/dashboards/dummy1/')


class ReportTests(TestCase):
    def test_id(self):
        dr1 = DummyReport1({})
        self.assertEqual(dr1.id, 'dummy1')

    def test_template(self):
        dr1 = DummyReport1({})
        self.assertEqual(dr1.template, normcase('reports/dummy1.html'))
        dr3 = DummyReport3({})
        self.assertEqual(dr3.template, normcase('reports/dummy/dummy3.html'))

    def test_container_id(self):
        dr1 = DummyReport1({})
        self.assertEqual(dr1.container_id, 'dummy1_report')

    def test_get_raw_view_url(self):
        dr1 = DummyReport1({})
        self.assertEqual(dr1.get_raw_view_url(), '/reports/dummy1/raw/?')

        dr1 = DummyReport1({'param1': 123, 'param2': 'abc'})
        self.assertEqual(dr1.get_raw_view_url(), '/reports/dummy1/raw/?param1=123&param2=abc')
