from django.test import TestCase
from django.urls import reverse


class DashboardsViewTests(TestCase):
    def test_dashboard_home(self):
        response = self.client.get(reverse('bi:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '70% Increase in 30 Days')

    def test_dashboard_detail(self):
        response = self.client.get(reverse('bi:dashboard-detail', args=('dummy1',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dummy report 1')
        self.assertContains(response, 'Dummy report 2')

    def test_dashboard_detail_nested(self):
        response = self.client.get(reverse('bi:dashboard-detail-nested', args=('dummy1', 'dummy3',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dummy report 1')
        self.assertContains(response, 'Dummy report 2')

    def test_breadcrumbs_first_level(self):
        response = self.client.get(reverse('bi:dashboard-detail', args=('dummy1',)))
        # TODO: add all breadcrumbs (now doesn't work)
        # self.assertInHTML('<ol class="breadcrumb"><li><a href="/"><i class="fa fa-home"></i></a></li><li class="active">Dummy board 1</li></ol>', str(response.content))
        self.assertInHTML('<li><a href="/"><i class="fa fa-home"></i></a></li>', str(response.content))
        self.assertInHTML('<li class="active">Dummy board 1</li>', str(response.content))

    def test_breadcrumbs_second_level(self):
        response = self.client.get(reverse('bi:dashboard-detail-nested', args=('dummy1', 'dummy3',)))
        self.assertInHTML('<li><a href="/"><i class="fa fa-home"></i></a></li>', str(response.content))
        self.assertInHTML('<li><a href="/dashboards/dummy1/">Dummy board 1</a></li>', str(response.content))
        self.assertInHTML('<li class="active">Dummy board 3</li>', str(response.content))
