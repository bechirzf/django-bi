from django.test import TestCase

from bi.templatetags.gravatar import gravatar_url, gravatar


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
