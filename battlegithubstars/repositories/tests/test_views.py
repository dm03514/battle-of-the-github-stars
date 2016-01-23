from unittest.mock import Mock
from django.forms import forms
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from repositories.utils import GitHubAPIError
from repositories.views import GitHubBattleFormView


class GithubBattleFormViewTestCase(TestCase):

    def test_github_battle_form_view_get_success(self):
        """
        Tests that github battle form view returns 200

        :return:
        """
        response = self.client.get(reverse('repositories:githubbattle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('github_battle_form_view.html')

    def test_render_form_error_on_get_repo_failure(self):
        """
        Tests that form is rendered with error on GitHubAPI error

        :return:
        """
        mock_request_class = Mock()
        mock_client = mock_request_class.return_value
        mock_client.get_repo.side_effect = GitHubAPIError()

        class GHBFTestView(GitHubBattleFormView):
            github_client_class = mock_request_class

        view = GHBFTestView()
        mock_repos = {
            'repo1': {
                'path': '', 'url': 'repo1'
            }
        }
        factory = RequestFactory()
        request = factory.get(reverse('repositories:githubbattle'))
        view.request = request

        mock_form = Mock(
            cleaned_data=mock_repos
        )
        response = view.form_valid(form=mock_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('github_battle_form_view.html')
        mock_form._errors.setdefault.assert_called_once_with(
            forms.NON_FIELD_ERRORS,
            GitHubBattleFormView.GITHUB_API_ERROR_MESSAGE.format('repo1')
        )

    def test_form_valid_gets_multiple_repos_and_renders_template(self):
        """
        Tests that when form contains multiple repos get_repo will be
        used to fetch the repos and they will be rendered with
        repo_comparison.html
        """
        mock_request_class = Mock()
        mock_client = mock_request_class.return_value
        mock_client.get_repo.side_effect = [
            'repo1processed', 'repo2processed'
        ]

        class GHBFTestView(GitHubBattleFormView):
            github_client_class = mock_request_class
            FILTERED_KEYS = ()

        factory = RequestFactory()
        request = factory.get(reverse('repositories:githubbattle'))
        view = GHBFTestView()
        view.request = request

        mock_repos = {
            'repo1': {
                'path': '', 'url': 'repo1'
            },
            'repo2': {
                'path': '', 'url': 'repo2'
            }
        }
        response = view.form_valid(form=Mock(
            cleaned_data=mock_repos
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('repo_comparison.html')

    def test_filter_repo_limits_keys(self):
        """
        Tests that filter_repo filters keys that are not in KEYS tuple

        :return:
        """
        repo_dict = {
            'stargazers_count': 1,
            'watchers_count': 1,
            'forks_count': 1,
            'strip_me': 'here',
            'remove': 'this'
        }

        expected = {
            'stargazers_count': 1,
            'watchers_count': 1,
            'forks_count': 1,
        }

        self.assertEqual(
            GitHubBattleFormView.filter_repo(repo_dict),
            expected
        )
