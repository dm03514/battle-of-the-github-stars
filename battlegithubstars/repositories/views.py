from django.core.urlresolvers import reverse_lazy
from django.forms import forms
from django.shortcuts import render
from django.views.generic.edit import FormView
from repositories.forms import GitHubBattleForm
from repositories.utils import GitHubAPIClient, GitHubAPIError


class GitHubBattleFormView(FormView):
    template_name = 'github_battle_form_view.html'
    form_class = GitHubBattleForm
    github_client_class = GitHubAPIClient
    FILTERED_KEYS = (
        'stargazers_count',
        'watchers_count',
        'forks_count',
    )
    GITHUB_API_ERROR_MESSAGE = 'Error fetching info for {} from github API'

    def form_valid(self, form):
        """
        Gathers github stats on the submitted repository and
        renders a template to compare them.

        This VIOLATES Post/redirect/get in return for a simpler
        architecture.

        :param form:
        :return:
        """
        # get github data
        client = self.github_client_class()
        repos = []
        try:
            for form_field, repo_info in form.cleaned_data.items():
                repos.append(
                    (repo_info['url'], client.get_repo(repo_info['path']))
                )
        except GitHubAPIError as e:
            # application is aware of this error, but don't do anything
            # in the case it's thrown
            form._errors.setdefault(
                forms.NON_FIELD_ERRORS,
                self.GITHUB_API_ERROR_MESSAGE.format(repo_info['url'])
            )
            return self.form_invalid(form)

        context = {
            'repos': [(url, self.filter_repo(repo)) for url, repo in repos]
        }

        return render(
            self.request, 'repo_comparison.html', context)

    @classmethod
    def filter_repo(cls, repo_dict):
        """
        Returns a repo with only a couple of fields displayed:
        Star count, watcher count, and fork count
        :param repo_dict:
        :return:
        """
        filtered_dict = {}
        for key in cls.FILTERED_KEYS:
            filtered_dict[key] = repo_dict[key]
        return filtered_dict

