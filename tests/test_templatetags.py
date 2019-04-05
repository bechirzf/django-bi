from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bi.templatetags.gravatar import gravatar_url, gravatar
from tests.fixtures.objects.reports.dummy1 import Report as DummyReport1
from tests.fixtures.objects.reports.dummy2 import Report as DummyReport2


class TemplateTagsTests(TestCase):

    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com',
                                             'temporary')

    def test_gravatar_url(self):
        self.assertEqual(
            gravatar_url('zhelyabuzhsky@icloud.com', 160),
            'https://www.gravatar.com/avatar/0284c304e6e8f0de6cfa8d7bed45d3aa?s=160'
        )

    def test_gravatar(self):
        self.assertHTMLEqual(
            gravatar('zhelyabuzhsky@icloud.com', 160),
            '<img src="https://www.gravatar.com/avatar/0284c304e6e8f0de6cfa8d7bed45d3aa?s=160" height="160" width="160">'
        )

    def test_report(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get(
            reverse('bi:dashboard-detail', args=('dummy1',)), follow=True)
        self.assertTemplateUsed(response, DummyReport1({}).template)
        self.assertTemplateUsed(
            response,
            DummyReport2({
                'param1': 'abc',
                'param2': 123
            }).template)
