from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse

from bi.templatetags.gravatar import gravatar_url, gravatar
from bi.tests.fixtures.objects.reports.dummy1.report import Report as DummyReport1


class TemplateTagsTests(TestCase):
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
        response = self.client.get(reverse('bi:dashboard-detail', args=('dummy1',)))
        self.assertTemplateUsed(response, DummyReport1(QueryDict()).template)
