import requests


class GitHubAPIError(Exception):
    pass


class GitHubAPIClient:
    """
    Small wrapper around the github api client tha makes request through
    'request' library, by default.
    """
    def __init__(self, request_lib=requests):
        self.request_lib = request_lib

    def get_repo(self, repo_path_info):
        """
        Makes a request to github for a repo
        :param repo_info:
        :return: Dict
        :raises: GitHubAPIError
        """
        api_url = self.build_github_url(repo_path_info)
        response = self.request_lib.get(api_url)
        if response.ok:
            return response.json()
        else:
            raise GitHubAPIError()

    @staticmethod
    def build_github_url(repo_path_info):
        return 'https://api.github.com/repos/{USER}/{REPOSITORY}'.format(
            **repo_path_info)
