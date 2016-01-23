from unittest.mock import Mock
from django.test import TestCase
from repositories.utils import GitHubAPIClient, GitHubAPIError


class GitHubAPIClientTestCase(TestCase):
    def test_build_github_url_success(self):
        repo_info = {
            'USER': 'dm03514',
            'REPOSITORY': 'test-repo'
        }
        api_url = GitHubAPIClient.build_github_url(repo_info)
        self.assertEqual(
            api_url,
            'https://api.github.com/repos/dm03514/test-repo'
        )

    def test_get_repo_response_not_ok(self):
        """
        Tests that when response is not ok GitHubAPIError is raised.

        :return:
        """
        mock_response = Mock()
        mock_response.ok = False

        mock_request = Mock()
        mock_request.get.return_value = mock_response
        client = GitHubAPIClient(request_lib=mock_request)
        repo_info = {
            'USER': 'test',
            'REPOSITORY': 'test-test'
        }
        with self.assertRaises(GitHubAPIError):
            client.get_repo(repo_info)
