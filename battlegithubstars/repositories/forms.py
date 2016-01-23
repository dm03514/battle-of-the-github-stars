import re
from urllib.parse import urlparse
from django import forms
from django.core.exceptions import ValidationError


class URLPathExtractorField(forms.URLField):
    INVALID_NETLOCK_ERROR = 'URL: {}, Expected netloc of {}, received {}'

    def __init__(self, *args, **kwargs):
        self.netloc = kwargs.pop('netloc')
        self.path_regex = kwargs.pop('path_regex')
        super(URLPathExtractorField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """
        Validates the url, then compares the url netloc and extracts
        any path matches.

        :param value:
        :return: Dictionary
        """
        value = self.to_python(value).strip()
        cleaned_value = super(URLPathExtractorField, self).clean(value)
        url_parts = urlparse(cleaned_value)

        self._validate_netloc(url_parts, value)

        return {
            'url': cleaned_value,
            'path': self._extract_path(url_parts.path)
        }

    def _extract_path(self, path):
        """
        Matches the path regular expression against the path of the url.
        Returns all matches.

        :param path:
        :return: Dict
        """
        p = re.compile(self.path_regex)
        match = p.search(path)
        if match:
            return match.groupdict()

        return {}

    def _validate_netloc(self, url_parts, full_url):
        """
        Validates that the net_loc of the url submitted is equal
        to the expected netloc, that the field was instantiated with.

        :param url_parts:
        :param full_url:
        :raises: ValidationError
        :return:
        """
        if (url_parts.netloc != self.netloc):
            raise ValidationError(
                self.INVALID_NETLOCK_ERROR.format(
                    full_url, self.netloc, url_parts.netloc)
            )


class GitHubBattleForm(forms.Form):
    PATH_REGEX = r'^/(?P<USER>\w+)/(?P<REPOSITORY>[\w-]+)$'

    repo_1_url = URLPathExtractorField(
        netloc='github.com', path_regex=PATH_REGEX)
    repo_2_url = URLPathExtractorField(
        netloc='github.com', path_regex=PATH_REGEX)
