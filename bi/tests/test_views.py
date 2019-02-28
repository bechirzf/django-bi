from django.test import TestCase
from django.urls import reverse


class DashboardsViewTests(TestCase):
    def test_dashboard_detail(self):
        response = self.client.get(reverse('bi:dashboard-detail', args=('dummy1',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dummy report 1')
        self.assertContains(response, 'Dummy report 2')
