from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardsViewTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_dashboard_home(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('bi:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '70% Increase in 30 Days')

    def test_dashboard_detail(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('bi:dashboard-detail', args=('dummy1',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dummy report 1')
        self.assertContains(response, 'Dummy report 2')

    def test_dashboard_detail_nested(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('bi:dashboard-detail-nested', args=('dummy1', 'dummy3',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dummy report 1')
        self.assertContains(response, 'Dummy report 2')
        self.assertContains(response, 'Dummy report 3')
        self.assertContains(response, '<div id="dummy3-report-test-div"></div>', html=True)

    def test_breadcrumbs_first_level(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('bi:dashboard-detail', args=('dummy1',)))
        self.assertContains(
            response,
            '<ol class="breadcrumb"><li><a href="/"><i class="fa fa-home"></i></a></li><li class="active">Dummy board 1</li></ol>',
            html=True
        )

    def test_breadcrumbs_second_level(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('bi:dashboard-detail-nested', args=('dummy1', 'dummy3',)))
        self.assertContains(
            response,
            '<ol class="breadcrumb"><li><a href="/"><i class="fa fa-home"></i></a></li><li><a href="/dashboards/dummy1/">Dummy board 1</a></li><li class="active">Dummy board 3</li></ol>',
            html=True
        )


class ReportsViewTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_report_view(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/reports/dummy1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dummy report 1')

        response = self.client.get('/reports/dummy/dummy3/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dummy report 3')

    def test_report_raw_view(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/reports/dummy1/raw/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response).__name__, 'JsonResponse')

        response = self.client.get('/reports/dummy/dummy3/raw/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response).__name__, 'JsonResponse')

    def test_report_list(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(reverse('bi:report-list'))
        self.assertContains(
            response,
            '<ul><li><a href="/reports/dummy/dummy3/">Dummy report 3</a></li><li><a href="/reports/dummy1/">Dummy report 1</a></li><li><a href="/reports/dummy2/">Dummy report 2</a></li></ul>',
            html=True
        )
