from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import FormView
from repositories.forms import GitHubBattleForm
from repositories.utils import GitHubAPIClient, GitHubAPIError


class GitHubBattleFormView(FormView):
    template_name = 'github_battle_form_view.html'
    form_class = GitHubBattleForm
    github_client_class = GitHubAPIClient

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
        try:
            repos = [
                (repo_info['url'], client.get_repo(repo_info['path']))
                    for repo_info in form.cleaned_data.values()
            ]
        except GitHubAPIError as e:
            # application is aware of this error, but don't do anything
            # in the case it's thrown
            raise e

        context = {
            'repos': repos
        }

        return render(
            self.request, 'repo_comparison.html', context)
