from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from repositories.forms import URLPathExtractorField, GitHubBattleForm


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


class GitHubBattleFormTesCase(TestCase):

    def test_form_validates_with_two_valid_urls(self):
        """
        Tests that the form can validate and return the correct data.

        :return:
        """
        form_data = {
            'repo_1_url': 'https://github.com/dm03514/CraigslistGigs',
            'repo_2_url': 'https://github.com/dm03514/django-cbv-toolkit'
        }
        form = GitHubBattleForm(form_data)
        self.assertTrue(form.is_valid())
        expected = {
            'repo_2_url': {
                'path': {
                    'USER': 'dm03514',
                    'REPOSITORY': 'django-cbv-toolkit'
                },
                'url': 'https://github.com/dm03514/django-cbv-toolkit'
            },
            'repo_1_url': {
                'path': {
                    'USER': 'dm03514',
                    'REPOSITORY': 'CraigslistGigs'
                },
                'url': 'https://github.com/dm03514/CraigslistGigs'
            }
        }
        self.assertEqual(form.cleaned_data, expected)

    def test_form_is_invalid_when_one_url_is_valid(self):
        """
        Tests that form detects when one url is valid and the other isn't.

        :return:
        """
        form_data = {
            'repo_1_url': 'https://github.com/dm03514/CraigslistGigs',
            'repo_2_url': 'https://wrong.com/dm03514/django-cbv-toolkit'
        }
        form = GitHubBattleForm(form_data)
        self.assertFalse(form.is_valid())
