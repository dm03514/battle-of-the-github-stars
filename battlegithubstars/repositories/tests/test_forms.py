from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from repositories.forms import URLPathExtractorField


class URLPathExtractorFieldTestCase(TestCase):

    def test_detects_invalid_url(self):
        """
        Tests that the urlpathextractor field will detect an invalid url.

        :return:
        """
        url = 'hiinvalidurlhere'
        url_path_extractor = URLPathExtractorField(
            netloc='', path_regex=''
        )
        with self.assertRaises(ValidationError):
            try:
                url_path_extractor.clean(url)
            except ValidationError as e:
                self.assertEqual(e.messages, ['Enter a valid URL.'])
                raise e

    def test_detects_valid_url(self):
        """
        Tests that valid URL can be detected, matching the domain initialized with
        the field.

        :return:
        """
        url = 'https://github.com/dm03514/battle-of-the-github-stars'
        url_path_extractor = URLPathExtractorField(
            netloc='github.com',
            path_regex=r'^/(?P<USER>\w+)/(?P<REPOSITORY>[\w-]+)$'
        )
        results = url_path_extractor.clean(url)
        expected = {
            'url': url,
            'path': {
                'USER': 'dm03514',
                'REPOSITORY': 'battle-of-the-github-stars'
            }
        }
        self.assertEqual(results, expected)
